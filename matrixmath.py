import numpy as np
from typing import List

def multiply_transformations(matrices: List[np.ndarray]) -> np.ndarray:
    result = np.identity(4)
    for matrix in matrices:
        result = np.dot(result, matrix)
    return result

def rotation_matrix_x(angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,  0,  0],
        [0, c, -s,  0],
        [0, s,  c,  0],
        [0, 0,  0,  1]
    ], dtype=np.float32)

def rotation_matrix_y(angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [ c,  0, s,  0],
        [ 0,  1, 0,  0],
        [-s,  0, c,  0],
        [ 0,  0, 0,  1]
    ], dtype=np.float32)

def rotation_matrix_z(angle: float) -> np.ndarray:
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0,  0],
        [s,  c, 0,  0],
        [0,  0, 1,  0],
        [0,  0, 0,  1]
    ], dtype=np.float32)

def rotation_matrix_all(all_radians: np.ndarray) -> np.ndarray:
    return multiply_transformations([
        rotation_matrix_x(all_radians[0]), 
        rotation_matrix_y(all_radians[1]), 
        rotation_matrix_z(all_radians[2])]
    )

def rotation_matrix(radians: float, axis: np.ndarray) -> np.ndarray:
    return rotation_matrix(axis * radians)

def scale_matrix(scale: np.ndarray) -> np.ndarray:
    return np.array([
        [scale[0], 0,        0,        0],
        [0,        scale[1], 0,        0],
        [0,        0,        scale[2], 0],
        [0,        0,        0,        1]
    ], dtype=np.float32)

def translation_matrix(position: np.ndarray) -> np.ndarray:
    return np.array([
        [1, 0, 0, position[0]],
        [0, 1, 0, position[1]],
        [0, 0, 1, position[2]],
        [0, 0, 0, 1]
    ], dtype=np.float32)