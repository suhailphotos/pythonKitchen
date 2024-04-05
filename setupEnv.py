import sys
import os

def set_path():
    proj_paths=['',] ## list where I would add any extra paths if needed
    project_root = os.path.join(os.path.dirname(__file__), *proj_paths)

    if project_root not in sys.path:
        sys.path.append(project_root)
set_path()
