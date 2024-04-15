import csv
import json

def csv_to_json(csv_file, json_file):
    # Define the fieldnames as per your CSV columns
    fieldnames = ['file', 'file_path', 'source', 'scene', 'clouds', 'hour', 'color', 'resol', 'variant', 'new_file_name']
    
    # Initialize an empty dictionary to store data
    data = {"hdri": {}}

    # Read the CSV file and convert each row to a dictionary
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        # Skip header
        next(reader)
        for row in reader:
            # Use the 'file' column as the key for each entry
            key = row['file']
            # Remove the 'file' column from the row since it will be the key
            del row['file']
            # Add the row data to the dictionary
            data["hdri"][key] = row

    # Write the dictionary to a JSON file
    with open(json_file, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

# Usage example
csv_to_json('/Users/suhail/Documents/matrix/packages/pythonKitchen/pythonkitchen/hdriRen/file_rename.csv', '/Users/suhail/Documents/matrix/packages/pythonKitchen/pythonkitchen/hdriRen/hdri.json')

