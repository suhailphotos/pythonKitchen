import os
import shutil

def copy_files(src_dir, dest_dir):
    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)
    
    # Initialize a counter for duplicate files
    duplicate_counter = {}
    
    # Iterate over files and directories in the source directory
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            # Get the source file path
            src_file_path = os.path.join(root, file)
            
            # Get the destination file path by joining the destination directory with the file name
            dest_file_path = os.path.join(dest_dir, file)
            
            # Check if the file already exists in the destination directory
            if os.path.exists(dest_file_path):
                # If the file exists, add a suffix to make it unique
                base, ext = os.path.splitext(file)
                if base in duplicate_counter:
                    duplicate_counter[base] += 1
                else:
                    duplicate_counter[base] = 1
                new_file_name = f"{base}_{duplicate_counter[base]}{ext}"
                dest_file_path = os.path.join(dest_dir, new_file_name)
            
            # Copy the file to the destination directory
            shutil.copy2(src_file_path, dest_file_path)
            print(f"Copied {src_file_path} to {dest_file_path}")

# Define source and destination directories
source_directory = '/Users/suhail/Library/CloudStorage/Dropbox/threeD/lib/hdri'  # Replace with the path to your source directory
destination_directory = '/Users/suhail/Library/CloudStorage/Dropbox/threeD/lib/temp_hdir'  # Replace with the path to your destination directory

# Call the function to copy files
copy_files(source_directory, destination_directory)

