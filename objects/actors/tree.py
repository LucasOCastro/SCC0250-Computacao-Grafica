from objects.object import Object
from objects.primitives import Cube, Cylinder, Sphere
import numpy as np

class Tree(Object):
    TRUNK_COLOR = (0.4, 0.2, 0.0, 1.0)

    LEAF_COLORS = [
        (0.3647, 0.5294, 0.2118, 1.0),
        (0.5020, 0.6157, 0.2353, 1.0),
    ]

    def __init__(self, trunk_height=2.5, trunk_radius=0.3, leaf_count=5):
        super().__init__()

        self.trunk_height = trunk_height
        self.trunk_radius = trunk_radius
        self.leaf_count = leaf_count

        self.trunk = self._make_trunk(trunk_height, trunk_radius)
        self.leaves = self._make_leaves()
        self.children = [self.trunk, *self.leaves]

    def _make_trunk(self, height, radius):
        trunk = Cylinder(length=height, radius=radius)
        trunk.set_single_color(self.TRUNK_COLOR)
        return trunk
    
    def _make_leaf_sphere(self, offset, radius):
        """Cria uma folha esférica de cor aleatória com um offset"""
        color = Tree.LEAF_COLORS[np.random.randint(0, len(self.LEAF_COLORS))]
        sphere = Sphere(color=color, radius=radius)

        origin = np.array([0.0, self.trunk_height / 2, 0.0])        
        sphere.set_pos(origin + offset)

        return sphere
    
    def _make_leaf_ring(self, count, sphere_radius, ring_radius, y_offset):
        """Cria um anel de folhas esféricas em uma determinada altura em relação ao topo do tronco"""
        leaves = []
        angle_step = 2*np.pi / count
        for i in range(count):
            angle = angle_step * i
            offset = np.array([np.cos(angle), 0, np.sin(angle)]) * ring_radius
            offset[1] = y_offset
            leaves.append(self._make_leaf_sphere(offset, sphere_radius))

        return leaves
    
    def _make_leaves(self):
        """Cria as folhas do arvore"""
        leaves = []

        # Cria 2 aneis de folhas e 1 folha central
        leaves.extend(self._make_leaf_ring(5, .6, .5, -.5))
        leaves.extend(self._make_leaf_ring(3, .5, .35, 0))
        leaves.extend(self._make_leaf_ring(1, .4, 0, 0.35))
        return leaves