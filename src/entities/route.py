from copy import copy
from typing import List, Set, Dict

from .nodes import Parking, GeoNode, Warehouse
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

    @property
    def prod_names(self) -> Set[str]:
        names: Set[str] = set()
        for load in self.loads:
            for prod in load:
                names.add(prod.name)
        return names

    @property
    def warehouse(self) -> Warehouse:
        for node, load in zip(self.nodes, self.loads):
            if isinstance(node, Warehouse) and not load.is_empty():
                return node

    @property
    def products(self):
        index = self.nodes.index(self.warehouse)
        return self.loads[index]

    @property
    def node_dist(self) -> Dict[GeoNode, float]:
        dist = 0.0
        dist_dict = {self.nodes[0]: dist}

        for node_form, node_to in zip(self.nodes[:-1], self.nodes[1:]):
            road = node_form.linked[node_to]
            dist += road.dist
            dist_dict[node_to] = dist

        return dist_dict
