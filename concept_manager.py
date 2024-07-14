# concept_manager.py
import json
import os

concepts_file = 'concepts.json'

def load_concepts():
    if os.path.exists(concepts_file):
        with open(concepts_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_concepts(concepts):
    with open(concepts_file, 'w', encoding='utf-8') as file:
        json.dump(concepts, file, indent=2)

concepts = load_concepts()

def add_concept(concept_name, keywords):
    concepts[concept_name] = keywords
    save_concepts(concepts)

def remove_concept(concept_name):
    if concept_name in concepts:
        del concepts[concept_name]
        save_concepts(concepts)

def modify_concept(concept_name, keywords):
    concepts[concept_name] = keywords
    save_concepts(concepts)
