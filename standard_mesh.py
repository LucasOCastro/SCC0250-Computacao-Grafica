import os
import numpy as np
from PIL import Image

DECIMAL_PLACES = 6

def merge_textures(mat_dir: str, textures_dir: str) -> tuple[Image.Image, dict[str, tuple[tuple[int, int], tuple[int, int]]]]:
    """
    Merge all textures into a single image.
    Returns:
    - Image.Image: The final image.
    - dict[str, tuple[tuple[int, int], tuple[int, int]]]: A dictionary mapping material names to their position and size in the final image.
    """
    final_image = Image.new('RGB', (0, 0))
    current_image_name = None
    current_image_pos = np.array([0, 0])
    pos_size_dict = {}

    def handle_textureless_material():
        # TODO treat material with no texture properly, currently just sets to 0,0
        if current_image_name is not None:
            print(f'No texture for {current_image_name}')
            pos_size_dict[current_image_name] = ((0, 0), (0, 0))

    with open(mat_dir, 'r') as file:
        for line in file:
            if line.startswith('newmtl'):
                handle_textureless_material()
                current_image_name = line.split()[1]
            elif line.startswith('map_Kd') and current_image_name is not None:
                og_path = " ".join(line.split()[1:])
                file_name = os.path.basename(og_path)
                img_path = os.path.join(textures_dir, file_name)

                # TODO consider expanding verticaly as well, maybe even packing
                with Image.open(img_path) as img:
                    new_height = max(img.size[1], final_image.size[1])
                    new_width = final_image.size[0] + img.size[0]
                    new_final_image = Image.new('RGB', (new_width, new_height))
                    new_final_image.paste(final_image, (0, 0))
                    new_final_image.paste(img, tuple(current_image_pos.tolist()))
                    final_image = new_final_image

                img_pos = current_image_pos.copy()
                img_size = np.array(img.size)
                pos_size_dict[current_image_name] = (img_pos, img_size)
                current_image_pos[0] += img.size[0]

                # Clear current image name
                current_image_name = None
    handle_textureless_material()
    return final_image, pos_size_dict

def circular_sliding_window_of_three(arr: list) -> list:
    if len(arr) == 3:
        return arr
    
    circular_arr = arr + [arr[0]]
    result = []
    for i in range(len(circular_arr) - 2):
        result.extend(circular_arr[i:i+3])
    return result

def filter_obj(obj_dir: str) -> tuple[list[tuple[float]], list[tuple[float]], dict[str, list[str]]]:
    """
    Read an obj file and return a raw list of relevant v, vt, f, usemtl lines.
    Returns:
    - list[tuple[float]]: v - A list of vertices.
    - list[tuple[float]]: vt - A list of texture coordinates.
    - dict[str, list[tuple[int]]]: f - A dictionary mapping material names to a list of face lines.
    """
    raw_vertex_list = []
    raw_vt_list = []
    mat_to_faces = {}
    current_mat = None
    with open(obj_dir, "r") as file:
        for line in file:
            values = line.split()
            if not values:
                continue

            if values[0] == 'v':
                raw_vertex_list.append(values[1:4])
            elif values[0] == 'vt':
                raw_vt_list.append(values[1:3])
            elif values[0] == 'usemtl':
                if values[1] not in mat_to_faces:
                    mat_to_faces[values[1]] = []
                current_mat = values[1]
            elif values[0] == 'f':
                face = tuple(values[1:])
                mat_to_faces[current_mat].append(face)
    return raw_vertex_list, raw_vt_list, mat_to_faces       

def reprocess_obj(mesh_name: str, root_dir: str) -> None:
    """
    Reprocess an obj and its mtl to have a single output texture and obj.
    
    The function takes an obj file and its mtl, and outputs a new obj file and a single png image. 
    The obj file is filtered to have unique vt coordinates, and the mtl file is merged into a single texture image.
    The vt coordinates are then remapped to the new texture image.
    
    Returns:
    None
    """
    # Get input directories
    obj_dir = os.path.join(root_dir, mesh_name + '.obj')
    mat_dir = os.path.join(root_dir, mesh_name + '.mtl')
    textures_dir = os.path.join(root_dir, 'textures')

    # Get output directories and make sure the folder exists
    output_dir = os.path.join(root_dir, 'output')
    output_obj_dir = os.path.join(output_dir, mesh_name + '.obj')
    output_tex_dir = os.path.join(output_dir, mesh_name + '.png')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Merge textures
    final_image, pos_size_dict = merge_textures(mat_dir, textures_dir)
    final_image.save(output_tex_dir)

    # Filter obj
    raw_vertex_list, raw_vt_list, mat_to_faces = filter_obj(obj_dir)
    
    new_vertex_list = raw_vertex_list
    new_vt_map = {}
    new_faces_list = []

    for mat, mat_faces in mat_to_faces.items():
        for line in mat_faces:
            new_face = []
            for face in line:
                parts = face.split('/')

                # If negative, is from end of array
                vt_index = int(parts[1])
                if vt_index < 0:
                    vt_index += len(raw_vt_list) + 1

                # Get the texture coordinates in the final merged image
                pos, size = pos_size_dict[mat]
                vt_local_normalized = raw_vt_list[vt_index - 1]
                vt_local_img = np.array(vt_local_normalized, dtype=np.float32) * np.array(size, dtype=np.float32)
                vt_final_img = vt_local_img + pos
                vt_final_normalized = vt_final_img / np.array(final_image.size, dtype=np.float32)

                # Get the index of the new texture coordinates, maintaining unicity
                new_vt_key = tuple(np.round(vt_final_normalized, decimals=DECIMAL_PLACES))
                new_vt_index = None
                if new_vt_key in new_vt_map:
                    new_vt_index = new_vt_map[new_vt_key]
                else:
                    new_vt_index = len(new_vt_map) + 1
                    new_vt_map[new_vt_key] = new_vt_index
                new_face.append(f'{parts[0]}/{new_vt_index}')
            # Record the new face
            new_faces_list.append(new_face)

    # Write new obj
    with open(output_obj_dir, 'w') as out_file:
        for vertex in new_vertex_list:
            out_file.write(f'v {vertex[0]} {vertex[1]} {vertex[2]}\n')
        for uv in new_vt_map.keys():
            out_file.write(f'vt {uv[0]} {uv[1]}\n')
        for face in new_faces_list:
            face = circular_sliding_window_of_three(face)
            tris = np.array(face).reshape(-1, 3)
            for tri in tris:
                out_file.write(f'f {tri[0]} {tri[1]} {tri[2]}\n')

root_dir = input("Caminho pra pasta com os arquivos .obj e .mtl: ").rstrip()
mesh_name = input("Nome do arquivo .obj e .mtl: ").rstrip()
reprocess_obj(mesh_name, root_dir)