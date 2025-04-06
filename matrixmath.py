import numpy as np
from typing import List

def multiply_transformations(matrices: List[np.ndarray]) -> np.ndarray:
    """Multiplica uma lista de matrizes de transformação 4x4 em ordem."""
    result = np.identity(4)
    for matrix in matrices:
        result = np.dot(result, matrix)
    return result

def rotation_matrix_x(angle: float) -> np.ndarray:
    """Gera matriz de rotação 4x4 em torno do eixo X (ângulo em radianos)."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,  0,  0],
        [0, c, -s,  0],
        [0, s,  c,  0],
        [0, 0,  0,  1]
    ], dtype=np.float32)

def rotation_matrix_y(angle: float) -> np.ndarray:
    """Gera matriz de rotação 4x4 em torno do eixo Y (ângulo em radianos)."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [ c,  0, s,  0],
        [ 0,  1, 0,  0],
        [-s,  0, c,  0],
        [ 0,  0, 0,  1]
    ], dtype=np.float32)

def rotation_matrix_z(angle: float) -> np.ndarray:
    """Gera matriz de rotação 4x4 em torno do eixo Z (ângulo em radianos)."""
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0,  0],
        [s,  c, 0,  0],
        [0,  0, 1,  0],
        [0,  0, 0,  1]
    ], dtype=np.float32)

def rotation_matrix_all(all_radians: np.ndarray) -> np.ndarray:
    """Gera matriz de rotação composta em torno de todos os eixos (ângulos em radianos)."""
    return multiply_transformations([
        rotation_matrix_x(all_radians[0]), 
        rotation_matrix_y(all_radians[1]), 
        rotation_matrix_z(all_radians[2])]
    )

def rotation_matrix(radians: float, axis: np.ndarray) -> np.ndarray:
    """Gera matriz de rotação em torno de um eixo arbitrário (em radianos)."""
    return rotation_matrix_all(axis * radians)

def scale_matrix(scale: np.ndarray) -> np.ndarray:
    """Gera matriz de escala 4x4 a partir do vetor [x, y, z]."""
    return np.array([
        [scale[0], 0,        0,        0],
        [0,        scale[1], 0,        0],
        [0,        0,        scale[2], 0],
        [0,        0,        0,        1]
    ], dtype=np.float32)

def translation_matrix(position: np.ndarray) -> np.ndarray:
    """Gera matriz de translação 4x4 a partir do vetor [x, y, z]."""
    return np.array([
        [1, 0, 0, position[0]],
        [0, 1, 0, position[1]],
        [0, 0, 1, position[2]],
        [0, 0, 0, 1]
    ], dtype=np.float32)