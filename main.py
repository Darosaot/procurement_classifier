import os
from data_loader import load_and_preprocess_data
from admin_interface import admin_interface

def main():
    data_dir = '/Users/dani/Desktop/Datos_código/Procurement_analyser/data'
    
    # Dynamically load all JSON files in the directory
    data_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

    all_data = []
    for data_file in data_files:
        data_path = os.path.join(data_dir, data_file)
        if os.path.isfile(data_path):  # Check if file exists
            data = load_and_preprocess_data(data_path)
            all_data.extend(data)
        else:
            print(f"File not found: {data_path}")

    # Start the admin interface
    admin_interface(all_data)

if __name__ == "__main__":
    main()
