import os
import streamlit as st
import pandas as pd
import logging
from data_loader import load_and_preprocess_data
from concept_manager import add_concept, remove_concept, modify_concept, concepts
from classifier import classify_text

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    st.title("Procurement Data Classifier")
    
    data_dir = 'data'
    
    # Dynamically get all JSON file paths in the directory
    data_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith('.json')]

    st.header("1. Manage Concepts")

    if st.button("Load Existing Concepts"):
        st.write(concepts)

    concept_name = st.text_input("Enter concept name:")
    keywords = st.text_input("Enter keywords (comma-separated):")

    if st.button("Add Concept"):
        add_concept(concept_name, [k.strip() for k in keywords.split(',')])
        st.write(f"Added concept '{concept_name}' with keywords: {keywords}")

    if st.button("Remove Concept"):
        remove_concept(concept_name)
        st.write(f"Removed concept '{concept_name}'")

    if st.button("Modify Concept"):
        modify_concept(concept_name, [k.strip() for k in keywords.split(',')])
        st.write(f"Modified concept '{concept_name}' with keywords: {keywords}")

    st.header("2. Classify Tenders")
    if st.button("Classify Tenders"):
        logger.info("Starting tender classification...")
        classified_data, total_time = load_and_preprocess_data(data_files)
        st.session_state['classified_data'] = classified_data
        st.write("Tenders Classified")
        st.write(f"Total loading and processing time: {total_time:.2f} seconds")
        logger.info(f"Tender classification completed in {total_time:.2f} seconds.")

    st.header("3. Basic Statistics")
    if 'classified_data' in st.session_state:
        classified_data = st.session_state['classified_data']
        concept_counts = {concept: 0 for concept in concepts.keys()}
        total_value = {concept: 0 for concept in concepts.keys()}

        for item in classified_data:
            classification = item['classification']
            for concept in classification:
                concept_counts[concept] += 1
                value = item.get('releases', [{}])[0].get('tender', {}).get('value', {}).get('amount', 0)
                total_value[concept] += value

        st.write("Number of entries per concept:")
        st.write(concept_counts)
        
        st.write("Total value per concept:")
        st.write(total_value)

    st.header("4. Visualize Classified Tenders")
    
    selected_concepts = st.multiselect(
        "Select concepts to display",
        options=list(concepts.keys())
    )

    if st.button("Show Classified Tenders"):
        try:
            tender_data = []
            if 'classified_data' in st.session_state:
                for idx, item in enumerate(st.session_state['classified_data'], start=1):
                    release = item.get('releases', [{}])[0]
                    tender = release.get('tender', {})
                    buyer = release.get('buyer', {})
                    item_concepts = item['classification']
                    if any(concept in selected_concepts for concept in item_concepts):
                        tender_data.append({
                            'Index': idx,
                            'Buyer Name': buyer.get('name', ''),
                            'Title': tender.get('title', ''),
                            'Description': tender.get('description', ''),
                            'Value': tender.get('value', {}).get('amount', 0),
                            'Currency': tender.get('value', {}).get('currency', ''),
                            'Award Criteria': tender.get('awardCriteria', ''),
                            'Concepts': ', '.join(item_concepts)
                        })
                
                tender_df = pd.DataFrame(tender_data).set_index('Index')
                st.dataframe(tender_df)
            else:
                st.write("No classified tenders to show.")
        except Exception as e:
            st.write(f"Error displaying classified tenders: {e}")
            logger.error(f"Error displaying classified tenders: {e}")

if __name__ == "__main__":
    main()