from copy import copy
from typing import List

from .nodes import Parking, GeoNode
from .product import ProductList
from .road import Road
from .transport import Transport


class Route:
    nodes: List[GeoNode]
    track: Transport | None
    loads: List[ProductList]

    def __init__(self, parking: Parking, *nodes: GeoNode):
        self.track = None
        self.nodes = [parking]
        self.loads = [ProductList()]

        for node in nodes:
            self.add_node(node)

    def __copy__(self) -> 'Route':
        new_route = Route(*self.nodes)
        new_route.loads = copy(self.loads)
        return new_route

    def __repr__(self) -> str:
        s = ' -> '.join(map(str, self.nodes))
        return s

    def add_node(self, node: GeoNode):
        if self.nodes[-1].is_linked(node):
            self.nodes.append(node)
            self.loads.append(ProductList())
        else:
            raise Exception('No road for next node')

    def set_track(self, track: Transport):
        self.track = track

    def set_load(self, node: GeoNode, load: ProductList):
        i = self.nodes.index(node)
        self.loads[i] = load

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
