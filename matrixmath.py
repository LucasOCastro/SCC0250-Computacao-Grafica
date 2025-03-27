import numpy as np

def multiply_transformations(matrices):
    result = np.identity(4)
    for matrix in matrices:
        result = np.dot(result, matrix)
    return result

def rotation_matrix_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,  0,  0],
        [0, c, -s,  0],
        [0, s,  c,  0],
        [0, 0,  0,  1]
    ], dtype=np.float32)

def rotation_matrix_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [ c,  0, s,  0],
        [ 0,  1, 0,  0],
        [-s,  0, c,  0],
        [ 0,  0, 0,  1]
    ], dtype=np.float32)

def rotation_matrix_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0,  0],
        [s,  c, 0,  0],
        [0,  0, 1,  0],
        [0,  0, 0,  1]
    ], dtype=np.float32)

def scale_matrix(scale):
    return np.array([
        [scale[0], 0,        0,        0],
        [0,        scale[1], 0,        0],
        [0,        0,        scale[2], 0],
        [0,        0,        0,        1]
    ], dtype=np.float32)

def translation_matrix(position):
    return np.array([
        [1, 0, 0, position[0]],
        [0, 1, 0, position[1]],
        [0, 0, 1, position[2]],
        [0, 0, 0, 1]
    ], dtype=np.float32)