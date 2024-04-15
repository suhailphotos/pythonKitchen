import os
import csv

def create_csv(directory, source, scene, hour, color, output_file):
    # Open CSV file in write mode
    with open(output_file, 'w', newline='') as csvfile:
        # Define column names
        fieldnames = ['file', 'file_path', 'source', 'scene', 'hour', 'color', 'new_file_name']
        # Initialize CSV writer
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write header row
        writer.writeheader()
        
        # Iterate through files in the directory
        for file_name in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file_name)):
                continue
            file_path = os.path.join(directory, file_name)
            ext = os.path.splitext(file_name)[1]
            new_file_name = f'{source}_{scene}_{hour}_{color}{ext}'
            # Write row for each file
            writer.writerow({
                'file': file_name,
                'file_path': file_path,
                'source': source,
                'scene': scene,
                'hour': hour,
                'color': color,
                'new_file_name': new_file_name
            })

directory_path = '/Users/suhail/Library/CloudStorage/Dropbox/threeD/lib/temp_hdir'
source = "src01"
scene = "sce02"
hour = "hr01"
color = "col01"
output_file = "/Users/suhail/Documents/matrix/packages/pythonKitchen/pythonkitchen/hdriRen/output.csv"

create_csv(directory_path, source, scene, hour, color, output_file)

