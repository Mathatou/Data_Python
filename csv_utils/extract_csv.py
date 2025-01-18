import os
import zipfile

def extract_if_needed():
    csv_to_zip_path_list = [
        ('data/csv/flights.csv', 'data/compressed/flights.zip'),
        ('data/csv/airlines.csv', 'data/compressed/airlines.zip'),
        ('data/csv/states.csv', 'data/compressed/states.zip'),
        ('data/csv/airports.csv', 'data/compressed/airports.zip'),
    ]
    
    for csv_to_zip_path in csv_to_zip_path_list:
        csv_path = csv_to_zip_path[0]
        zip_path = csv_to_zip_path[1]
        
        if not os.path.exists(csv_path):
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extract(os.path.basename(csv_path), os.path.dirname(csv_path))
            print(f"Extracted {csv_path} from {zip_path}")
