from copy import copy, deepcopy
from typing import List, Set, Dict

from . import Consumer, LinkedRoad
from .nodes import GeoNode, Warehouse
from .product import ProductList
from .road import Road
from .transport import Transport


class Route:
    nodes: List[GeoNode]
    track: Transport | None
    loads: List[ProductList]

    def __init__(self, node: GeoNode, *nodes: GeoNode):
        self.track = None
        self.nodes = [node]
        self.loads = [ProductList()]

        for node in nodes:
            self.add_node(node)

    def __copy__(self) -> 'Route':
        new_route = Route(*self.nodes)
        new_route.loads = deepcopy(self.loads)
        return new_route

    def __repr__(self) -> str:
        s = ' -> '.join(map(str, self.nodes))
        return s

    def add_node(self, node: GeoNode):
        if self.tail.is_linked(node):
            self.nodes.append(node)
            self.loads.append(ProductList())
        else:
            raise Exception('No road for next node')

    def set_track(self, track: Transport):
        self.track = track

    def set_load(self, node: GeoNode, load: ProductList):
        i = self.nodes.index(node)
        self.loads[i] = load

    def extend(self, node: GeoNode) -> 'Route':
        new = copy(self)
        new.add_node(node)
        return new

    def prolong(self, other: 'Route'):
        offset = 1 if self.tail == other.head else 0
        self.nodes += other.nodes[offset:]
        self.loads += other.loads[offset:]

    def inverse(self) -> 'Route':
        new = copy(self)
        new.nodes = new.nodes[::-1]
        new.loads = new.loads[::-1]
        return new

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
    def roads_forward(self) -> List[LinkedRoad]:
        last_forward = self.last_delivery
        index = self.nodes.index(last_forward)
        roads: List[LinkedRoad] = []
        for from_node, to_node in zip(self.nodes[:index], self.nodes[1:index + 1]):
            if from_node == last_forward:
                break
            road = from_node.linked[to_node]
            roads.append(LinkedRoad(from_node, to_node, road.dist, road.time))

        return roads

    @property
    def roads_backward(self) -> List[LinkedRoad]:
        last_forward = self.last_delivery
        index = self.nodes.index(last_forward)
        roads: List[LinkedRoad] = []
        for from_node, to_node in zip(self.nodes[index:-1], self.nodes[index + 1:]):
            road = from_node.linked[to_node]
            roads.append(LinkedRoad(from_node, to_node, road.dist, road.time))

        return roads

    @property
    def volume(self) -> float:
        return sum(prod.sum_volume for prod in self.products)

    @property
    def occupancy(self) -> float:
        return self.volume / self.track.volume

    @property
    def prod_names(self) -> Set[str]:
        names: Set[str] = set()
        for load in self.loads:
            for prod in load:
                names.add(prod.name)
        return names

    @property
    def warehouse(self) -> Warehouse:
        return self.find_warehouse(empty_route=False)

    @property
    def last_delivery(self) -> GeoNode:
        for node, load in zip(reversed(self.nodes), reversed(self.loads)):
            if load: return node

    def find_warehouse(self, empty_route=False):
        for node, load in zip(self.nodes, self.loads):
            if isinstance(node, Warehouse) and (not load.is_empty() or empty_route):
                return node

    @property
    def head(self) -> GeoNode:
        return self.nodes[0]

    @property
    def tail(self) -> GeoNode:
        return self.nodes[-1]

    @property
    def ctail(self) -> Consumer:
        for node in self.nodes[::-1]:
            if isinstance(node, Consumer):
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

    def _take_over_same(self, other: 'Route') -> bool:
        warehouse_index = self.nodes.index(self.warehouse)
        for node, load in zip(other.nodes[::-1], other.loads[::-1]):
            if node == other.warehouse:
                return True

            self.nodes.append(node)
            self.loads.append(load)
            self.loads[warehouse_index].add(load)

            other.nodes.pop()
            other.loads.pop()
        return True

    def take_over(self, other: 'Route') -> bool:
        if self.warehouse == other.warehouse:
            return self._take_over_same(other)
        else:
            pass
