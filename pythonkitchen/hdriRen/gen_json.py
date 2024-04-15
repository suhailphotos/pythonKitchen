import os
import json

def initialize_json_data():
    return {"hdri": {}}

def add_file_entry(json_data, file_name, file_path, source, scene, hour, color):
    ext = os.path.splitext(file_name)[1]
    entry = {
        "file_path": file_path,
        "source": source,
        "scene": scene,
        "hour": hour,
        "color": color,
        "resolution":resol,
        "new_file_name": f'{source}_{scene}_{hour}_{resol}_{color}{ext}'
    }
    json_data["hdri"][file_name] = entry

def write_json_file(json_data, output_file):
    with open(output_file, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

directory_path = '/Users/suhail/Library/CloudStorage/Dropbox/threeD/lib/temp_hdir'  
source = "src01"
scene = "sce02"
hour = "hr01"
color = "col01"
resol = "4k"
output_file = "/Users/suhail/Documents/matrix/packages/pythonKitchen/pythonkitchen/hdriRen/hdri.json"

json_data = initialize_json_data()

# Iterate through files in the directory and add entries to JSON data
for file_name in os.listdir(directory_path):
    if os.path.isdir(os.path.join(directory_path, file_name)):
        continue
    file_path = os.path.join(directory_path, file_name)
    add_file_entry(json_data, file_name, file_path, source, scene, hour, color)

write_json_file(json_data, output_file)

