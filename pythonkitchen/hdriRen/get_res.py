import os
import csv
import OpenEXR

def get_exr_resolution(exr_file):
    # Open the EXR file
    exr = OpenEXR.InputFile(exr_file)
    # Get the header information
    header = exr.header()
    # Extract the resolution
    width = header['displayWindow'].max.x + 1
    height = header['displayWindow'].max.y + 1
    return width, height

def create_csv_with_resolutions(directory, output_file):
    # Open CSV file in write mode
    with open(output_file, 'w', newline='') as csvfile:
        # Define column names
        fieldnames = ['file', 'width', 'height']
        # Initialize CSV writer
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write header row
        writer.writeheader()
        
        # Iterate through files in the directory
        for file_name in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file_name)):
                continue
            file_path = os.path.join(directory, file_name)
            if file_path.endswith('.exr'):
                # Get resolution for EXR files
                width, height = get_exr_resolution(file_path)
                # Write row for each file
                writer.writerow({
                    'file': file_name,
                    'width': width,
                    'height': height
                })

directory_path = '/Users/suhail/Library/CloudStorage/Dropbox/threeD/lib/temp_hdir'  # Replace with the path to your directory
output_file = "/Users/suhail/Documents/matrix/packages/pythonKitchen/pythonkitchen/hdriRen/resolution.csv"  # Replace with the path to your output CSV file

create_csv_with_resolutions(directory_path, output_file)

