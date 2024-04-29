import json
import os
import re

# Load JSON files
def load_json(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def rename_hdri():
    parent_dir = os.path.abspath(os.path.join(__file__,'../..'))
    renamed_json_path = os.path.join(parent_dir, 'textures_renamed.json')
    renamed_json_data = load_json(renamed_json_path)
    for current_file_name, attribs in renamed_json_data['hdri'].items():
        resolution = attribs['resol']
        new_filename = re.sub(r'(_)([^_]+)(_v\d+)([^_a-zA-Z]+)(\.\w+$)', rf'1_{resolution}_\2\3\4\5', current_file_name)
        print(new_filename)


def main():
    rename_hdri()

if __name__=='__main__':
    main()
