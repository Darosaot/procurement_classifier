import json
import re
import logging
import streamlit as st
import time
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from classifier import classify_text

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text

def process_line(line):
    try:
        json_obj = json.loads(line)
        release = json_obj.get('releases', [{}])[0]
        tender = release.get('tender', {})
        title = tender.get('title', '')
        description = tender.get('description', '')

        combined_text = f"{title} {description}"
        processed_text = preprocess_text(combined_text)
        classification = classify_text(processed_text)

        if classification:
            json_obj['processed_text'] = processed_text
            json_obj['classification'] = classification
            return json_obj
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON: {line}")
    return None

def process_file(filepath):
    classified_data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            processed_item = process_line(line)
            if processed_item:
                classified_data.append(processed_item)
    return classified_data

def load_and_preprocess_data(filepaths):
    classified_data = []
    total_files = len(filepaths)
    
    progress_bar = st.progress(0)
    progress_text = st.empty()

    start_time = time.time()
    
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_file, filepath): filepath for filepath in filepaths}
        
        for idx, future in enumerate(as_completed(futures), start=1):
            filepath = futures[future]
            try:
                data = future.result()
                classified_data.extend(data)
            except Exception as e:
                logger.error(f"Error processing file {filepath}: {e}")
            
            progress = idx / total_files
            progress_bar.progress(progress)
            progress_text.text(f'Processing file {idx}/{total_files} - {int(progress * 100)}% complete')

    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"Total loading and processing time: {total_time:.2f} seconds")
    
    return classified_data, total_time
