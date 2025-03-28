import hou
import re

def kitbash_matfile_paths(kitname: str = 'MTM', new_dir: str = '$USD_LIB/assets/kitbash/mtm/tex/_publish/4k/'):
    kb3d_mtm = hou.node(f'/obj/KB3D_{kitname}')
    matnet_node = kb3d_mtm.node('matnet')
    for subnet in matnet_node.children():
        if subnet.type().name() == 'subnet':
            for mtlximage_node in subnet.children():
                if mtlximage_node.type().name()=='mtlximage':
                    file_parm = mtlximage_node.parm('file')
                    if file_parm is not None:
                        file_path = file_parm.rawValue()
                        pattern = re.compile(r"^.*?/([^/]+/[^/]+)/[^/]+$")
                        new_file_path = re.sub(pattern, new_dir, file_path) + re.search(r"[^/]+$", file_path).group()
                        file_parm.set(new_file_path)

kitbash_matfile_paths('MTM')
