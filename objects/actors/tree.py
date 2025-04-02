from objects.object import Object
from objects.primitives import Cube, Cylinder, Sphere
import numpy as np

class Tree(Object):
    TRUNK_COLOR = (0.4, 0.2, 0.0, 1.0)

    LEAF_COLORS = [
        (0.5804, 0.6510, 0.4824, 1),
        (0.3490, 0.4549, 0.2706, 1),
        (0.3961, 0.5059, 0.2784, 1),
        (0.4471, 0.5922, 0.3843, 1)
    ]

    LEAF_SPAWN_OFFSET_RANGE = np.array([0.5, 0.4, 0.5])

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
        color = Tree.LEAF_COLORS[np.random.randint(0, len(self.LEAF_COLORS))]
        sphere = Sphere(color=color, radius=radius)

        origin = np.array([0.0, self.trunk_height / 2, 0.0])        
        sphere.set_pos(origin + offset)

        return sphere
    
    def _make_leaf_ring(self, count, sphere_radius, ring_radius, y_offset):
        leaves = []
        angle_step = 2*np.pi / count
        for i in range(count):
            angle = angle_step * i
            offset = np.array([np.cos(angle), 0, np.sin(angle)]) * ring_radius
            offset[1] = y_offset
            leaves.append(self._make_leaf_sphere(offset, sphere_radius))

        return leaves
    
    def _make_leaves(self):
        leaves = []

        # leaves.extend(self._make_leaf_ring(5, .6, .6, -.6))
        # leaves.extend(self._make_leaf_ring(3, .6, .25, 0))

        leaves.extend(self._make_leaf_ring(5, .6, .5, -.5))
        leaves.extend(self._make_leaf_ring(3, .5, .35, 0))
        leaves.extend(self._make_leaf_ring(1, .4, 0, 0.35))
        return leaves