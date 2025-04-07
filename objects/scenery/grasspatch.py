import numpy as np
from objects.object import Object
from objects.meshobject import MeshObject
from objects.primitives import Cube

class GrassPatch(Object):
    # Constantes visuais e de distribuição da grama
    ROT_MIN = 0  # rotação mínima em graus
    ROT_MAX = 15  # rotação máxima em graus
    SCALE_MIN = np.array([0.01, 0.08, 0.02])  # escala mínima (bem fininha e baixa)
    SCALE_MAX = np.array([0.01, 0.12, 0.02])  # escala máxima (um pouco mais alta)
    POS_OFFSET_RANGE = np.array([0.05, 0, 0.01])  # deslocamento aleatório da posição
    COLORS = [  # variações de cor de grama
        (0.3647, 0.5294, 0.2118, 1.0),
        (0.5020, 0.6157, 0.2353, 1.0),
        (0.3882, 0.5294, 0.0745, 1.0),
        (0.3686, 0.4039, 0.0902, 1.0)
    ]


    def __init__(self, area_size: np.ndarray, line_count: int, count_per_line: int):
        super().__init__()

        self.area_size = area_size
        self.line_count = line_count
        self.count_per_line = count_per_line

        # Cria os cubos de grama individuais
        cubes = self._make_grass_cubes()
        if len(cubes) == 0:
            return

        # Mescla todos os cubos num único objeto para melhorar performance (draw call única)
        squashed = MeshObject.merge_meshes(cubes)
        self.children.append(squashed)

        # Destroi os cubos originais (já estão fundidos no mesh)
        for cube in cubes:
            cube.destroy()

    def _make_grass_cubes(self):
        area_start = -self.area_size / 2
        area_end = self.area_size / 2

        # Distância entre os cubos na grid
        pos_step = self.area_size / np.array([
            max(1, self.count_per_line - 1),
            1,
            max(1, self.line_count - 1)
        ])

        cubes = []
        for i in range(self.line_count):
            for j in range(self.count_per_line):
                # Escolhe uma cor aleatória entre as disponíveis
                color = self.COLORS[np.random.randint(len(self.COLORS))]
                grass = Cube(color=color)

                # Aplica rotação aleatória em Y
                rot = np.random.uniform(self.ROT_MIN, self.ROT_MAX)
                grass.set_rot_deg([0, rot, 0])

                # Aplica escala aleatória dentro do intervalo definido
                scale = np.random.uniform(self.SCALE_MIN, self.SCALE_MAX)
                grass.set_scale(scale)

                # Calcula a posição na grade + offset aleatório
                pos = area_start + np.array([j * pos_step[0], 0, i * pos_step[2]])
                if pos[0] > area_end[0] or pos[2] > area_end[2]:
                    break  # evita ultrapassar a área

                rand_off = np.random.uniform(-self.POS_OFFSET_RANGE, self.POS_OFFSET_RANGE)
                grass.set_pos(pos + rand_off)

                cubes.append(grass)

        return cubes