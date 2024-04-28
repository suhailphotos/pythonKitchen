import os
import json
import shutil

# Get the VFX_LIB environment variable
ASSET_INGEST_DIR = os.getenv('ASSET_INGEST_DIR')
VFX_LIB = os.getenv('VFX_LIB')

# Define the paths
ingest_folder = os.path.join(ASSET_INGEST_DIR, 'textures', 'hdri')
hdri_folder = os.path.join(VFX_LIB, 'hdri')
renamed_json_path = os.path.join(os.path.dirname(__file__), 'textures_renamed.json')

# Load JSON files
def load_json(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

# Rename files and update JSON
def rename_files_and_update_json():
    hdri_data = load_json('../hdri.json')
    naming_codes = load_json('../namingcodes.json')
    renamed_hdri_data = []

    for old_filename, attributes in hdri_data['hdri'].items():
        source = naming_codes['source'].get(attributes['source'], 'unknown')
        scene = naming_codes['scene'].get(attributes['scene'], 'unknown')
        clouds = naming_codes['clouds'].get(attributes['clouds'], 'unknown')
        hour = naming_codes['hour'].get(attributes['hour'], 'unknown')
        color = naming_codes['color'].get(attributes['color'], 'unknown')
        variant = attributes['variant']
        file_extension = old_filename.split('.')[-1]

        # Generate new file name
        new_filename = f'{source}_{scene}_{clouds}_{hour}_{color}_{variant}.{file_extension}'

        # Rename the file
        old_file_path = attributes['file_path']
        new_file_path = os.path.join(hdri_folder, new_filename)
        shutil.move(old_file_path, new_file_path)

        # Update JSON data
        attributes['file_path'] = new_file_path
        attributes['new_file_name'] = new_filename
        renamed_hdri_data.append({
            'new_file_name': new_filename,
            'source': source,
            'scene': scene,
            'clouds': clouds,
            'hour': hour,
            'color': color,
            'resol': attributes['resol'],
            'variant': variant,
            'old_file_name': old_filename
        })

    # Write the updated data back to the original file
    with open(renamed_json_path, 'w') as json_file:
        json.dump(renamed_hdri_data, json_file, indent=4)

    print(f"Files renamed and JSON updated successfully. Renamed data saved to '{renamed_json_path}'.")

# Main function
def main():
    rename_files_and_update_json()

if __name__ == "__main__":
    main()

