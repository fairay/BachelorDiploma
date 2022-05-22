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
        new_route.track = self.track
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
        i = len(self.nodes) - 1 - self.nodes[::-1].index(node)
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
    def cost(self) -> float:
        return self.dist

    @property
    def roads(self) -> List[Road]:
        roads = []
        for node_form, node_to in zip(self.nodes[:-1], self.nodes[1:]):
            roads.append(node_form.linked[node_to])
        return roads

    @property
    def roads_forward(self) -> List[LinkedRoad]:
        index = self.last_delivery
        roads: List[LinkedRoad] = []
        for from_node, to_node in zip(self.nodes[:index], self.nodes[1:index + 1]):
            road = from_node.linked[to_node]
            roads.append(LinkedRoad(from_node, to_node, road.dist, road.time))

        return roads

    @property
    def roads_backward(self) -> List[LinkedRoad]:
        index = self.last_delivery
        roads: List[LinkedRoad] = []
        for from_node, to_node in zip(self.nodes[index:-1], self.nodes[index + 1:]):
            road = from_node.linked[to_node]
            roads.append(LinkedRoad(from_node, to_node, road.dist, road.time))

        return roads

    @property
    def volume(self) -> float:
        return sum(prod.sum_volume for prod in self.products)

    @property
    def free_volume(self) -> float:
        return self.track.volume - self.volume

    @property
    def occupancy(self) -> float:
        return self.volume / self.track.volume

    @property
    def free_space(self) -> int:
        prod = self.products
        if not prod: return -1
        return max(0, int((self.track.volume - self.volume) / prod[0].volume + 1e-5))

    @property
    def is_full(self) -> bool:
        return self.free_space == 0
        prod = self.products
        if not prod: return False
        return self.volume + prod[0].volume >= self.track.volume + 1e-5

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
    def last_delivery(self) -> int:
        for index, load in enumerate(reversed(self.loads)):
            if load: return len(self.nodes) - 1 - index

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
    def products(self) -> ProductList:
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
        other_warehouse = other.warehouse
        other_warehouse_index = other.nodes.index(other_warehouse)
        warehouse_index = self.nodes.index(self.warehouse)

        for node, load in zip(other.nodes[::-1], other.loads[::-1]):
            if node == other_warehouse:
                return True

            transit = copy(load)
            rem = transit.to_restriction(self.free_volume)

            self.nodes.append(node)
            self.loads.append(transit)
            self.loads[warehouse_index].add(transit)
            other.loads[other_warehouse_index].minus(transit)

            if rem.amount:
                other.loads[-1] = rem
                return False
            else:
                other.nodes.pop()
                other.loads.pop()

        return True

    def _take_over_diff(self, other: 'Route') -> bool:
        warehouse_index = self.nodes.index(self.warehouse)
        other_warehouse = other.warehouse
        other_warehouse_index = other.nodes.index(other_warehouse)

        for node, load in zip(other.nodes[::-1], other.loads[::-1]):
            if node == other_warehouse:
                return True

            transit = load.from_balance(self.warehouse)
            rem = transit.to_restriction(self.free_volume)
            if not len(transit):
                return False
            load.minus(transit)
            rem.to_balance(self.warehouse)
            transit.to_balance(other_warehouse)

            self.nodes.append(node)
            self.loads.append(transit)
            self.loads[warehouse_index].add(transit)
            other.loads[other_warehouse_index].minus(transit)

            if load.amount:
                return False
            else:
                other.nodes.pop()
                other.loads.pop()

        return True

    def take_over(self, other: 'Route') -> bool:
        if self.warehouse == other.warehouse:
            return self._take_over_same(other)
        else:
            return self._take_over_diff(other)

    def rollback(self, other: 'Route'):
        self.nodes = other.nodes
        self.loads = other.loads
        self.track = other.track


class RouteList(list[Route]):
    def __copy__(self) -> 'RouteList':
        new = RouteList()
        for route in self:
            new.append(copy(route))
        return new

    @property
    def blank_routes(self) -> 'RouteList':
        return RouteList(filter(lambda r: not r.is_full, self))

    @property
    def sort_occupancy(self) -> 'RouteList':
        return RouteList(sorted(self, key=lambda r: r.occupancy))

    @property
    def cost(self) -> float:
        return sum(route.cost for route in self)

    @property
    def snapshot(self) -> Dict[Route, Route]:
        old_new: Dict[Route, Route] = {}
        for route in self:
            old_new[route] = copy(route)
        return old_new

    def by_tail(self, tail: GeoNode) -> 'RouteList':
        return RouteList(filter(lambda r: r.tail == tail, self))

    def rollback(self, snapshot: Dict[Route, Route]):
        for route in self:
            if route in snapshot:
                route.rollback(snapshot[route])
