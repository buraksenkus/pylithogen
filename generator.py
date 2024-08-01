from file_io import extract_image_name_from_path, save_file_to_path

from os import makedirs
from os.path import abspath

import numpy as np
from PIL import Image
from stl import mesh


def convert_to_grayscale(image_path):
    return Image.open(image_path).convert('L')


def create_height_map(img, min_height, max_height):
    grayscale = np.array(img)
    # Normalize the grayscale values to range between min_height and max_height
    height_map_local = min_height + (max_height - min_height) * (1 - grayscale / 255.0)
    return height_map_local


def create_mesh(height_map, scale):
    rows, cols = height_map.shape
    vertices = []
    faces = []

    # Create vertices
    for i in range(rows):
        for j in range(cols):
            vertices.append([j * scale, i * scale, height_map[i, j]])

    # Create faces (two triangles for each square in the grid)
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Create two triangles for each grid square
            idx = i * cols + j
            faces.append([idx, idx + 1, idx + cols])
            faces.append([idx + 1, idx + 1 + cols, idx + cols])

    # Convert to numpy arrays
    vertices = np.array(vertices)
    faces = np.array(faces)

    # Create the mesh
    height_mesh_local = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            height_mesh_local.vectors[i][j] = vertices[face[j], :]

    return height_mesh_local


def create_column_mesh(height_map, scale, min_height):
    rows, cols = height_map.shape
    vertices = []
    faces = []

    # Function to add vertices and faces for a single column
    def add_column(x, y, height):
        # Top vertices
        v0 = [x * scale, y * scale, height]
        v1 = [(x + 1) * scale, y * scale, height]
        v2 = [(x + 1) * scale, (y + 1) * scale, height]
        v3 = [x * scale, (y + 1) * scale, height]
        # Bottom vertices
        v4 = [x * scale, y * scale, min_height]
        v5 = [(x + 1) * scale, y * scale, min_height]
        v6 = [(x + 1) * scale, (y + 1) * scale, min_height]
        v7 = [x * scale, (y + 1) * scale, min_height]

        # Append vertices
        idx = len(vertices)
        vertices.extend([v0, v1, v2, v3, v4, v5, v6, v7])

        # Append faces (top, bottom, and four sides)
        faces.extend([
            [idx, idx + 1, idx + 2], [idx, idx + 2, idx + 3],  # Top
            [idx + 4, idx + 5, idx + 6], [idx + 4, idx + 6, idx + 7],  # Bottom
            [idx, idx + 1, idx + 5], [idx, idx + 5, idx + 4],  # Side 1
            [idx + 1, idx + 2, idx + 6], [idx + 1, idx + 6, idx + 5],  # Side 2
            [idx + 2, idx + 3, idx + 7], [idx + 2, idx + 7, idx + 6],  # Side 3
            [idx + 3, idx, idx + 4], [idx + 3, idx + 4, idx + 7]  # Side 4
        ])

    # Create columns for each pixel
    for i in range(rows):
        for j in range(cols):
            add_column(j, i, height_map[i, j])

    # Convert to numpy arrays
    vertices = np.array(vertices)
    faces = np.array(faces)

    # Create the mesh
    height_mesh_local = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            height_mesh_local.vectors[i][j] = vertices[face[j], :]

    return height_mesh_local


def generate(args):
    image_name = extract_image_name_from_path(args.image_path)

    image = convert_to_grayscale(args.image_path)
    full_path = abspath(f'results/{image_name}')
    makedirs(full_path, exist_ok=True)
    save_file_to_path(image, f'{full_path}/{image_name}_grayscale.png')

    height_map = create_height_map(image, args.min_height, args.max_height)

    if args.method == 'emboss':
        height_mesh = create_mesh(height_map, args.scale)
    elif args.method == 'column':
        height_mesh = create_column_mesh(height_map, args.scale, args.min_height)
    else:
        print(f'Unknown method: {args.method}')
        exit(1)

    save_file_to_path(height_mesh, f'results/{image_name}/{image_name}.stl')
