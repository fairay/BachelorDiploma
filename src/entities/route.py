from typing import List

from .nodes import Parking, GeoNode
from .road import Road


class Route:
    def __init__(self, parking: Parking, *nodes: GeoNode):
        self.nodes: List[GeoNode] = [parking]
        for node in nodes:
            self.add_node(node)

    def add_node(self, node: GeoNode):
        if self.nodes[-1].is_linked(node):
            self.nodes.append(node)
        else:
            raise Exception('No road for next node')

    @property
    def dist(self) -> float:
        d = 0.0
        for node_form, node_to in zip(self.nodes[:-1], self.nodes[1:]):
            d += node_form.dist(node_to)
        return d

    @property
    def roads(self) -> List[Road]:
        roads = []
        for node_form, node_to in zip(self.nodes[:-1], self.nodes[1:]):
            roads.append(node_form.linked[node_to])
        return roads
