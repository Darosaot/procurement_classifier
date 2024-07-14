# classifier.py
from concept_manager import concepts

def classify_text(text):
    classifications = []
    for concept, keywords in concepts.items():
        for keyword in keywords:
            if keyword in text:
                classifications.append(concept)
                break
    return classifications
