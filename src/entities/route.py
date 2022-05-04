from typing import List

from entities import Parking, GeoNode, Road


class Route:
    def __init__(self, parking: Parking):
        self.nodes: List[GeoNode] = [parking]

    def add_node(self, node: GeoNode):
        if self.nodes[-1].is_linked(node):
            self.nodes.append(node)
        else:
            raise Exception('No road for next row')

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
