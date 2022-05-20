from copy import copy
from typing import List, Optional, Union, TextIO, Dict

import jsonpickle

from entities.nodes import Warehouse, Parking, Consumer
from entities.nodes.geonode import GeoNode
from entities.road import Road
from entities.route import Route, RouteList
from entities.transport import Transport


class TransportSystem(object):
    def __init__(self):
        self.routes: List[Route] = []

        self.parking: Optional[Parking] = None
        self.warehouses: List[Warehouse] = []
        self.consumers: List[Consumer] = []

        self.con: float = 1.0
        self.vol = 0.1

    def save_json(self, file: TextIO):
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        json_str = jsonpickle.encode(self, indent=4, keys=True)
        file.write(json_str)

    @staticmethod
    def load_json(file: TextIO) -> 'TransportSystem':
        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)
        data = jsonpickle.decode(file.read(), keys=True)

        return data

    def init_balance(self, routes: RouteList = None):
        for wnode in self.warehouses:
            for prod in wnode.stock:
                wnode.balance[prod.name] = prod.amount

        for cnode in self.consumers:
            for prod in cnode.order:
                cnode.balance[prod.name] = -prod.amount

        if not routes:
            return

        for route in routes:
            for node, load in zip(route.nodes, route.loads):
                mult = -1 if isinstance(node, Warehouse) else 1
                for prod in load:
                    node.balance[prod.name] += mult * prod.amount

    def check_valid(self) -> None:
        if self.parking is None:
            raise Exception("No parking")
        elif not self.transport:
            raise Exception("No transport")

        for w_node in self.warehouses:
            if self.parking not in w_node.linked.keys():
                raise Exception(f'{w_node} not linked with parking')

        for c_node in self.consumers:
            if not len(c_node.linked):
                raise Exception(f'{c_node} has no roads')

    def add_warehouse(self, node: Warehouse, parking_road: Road = None):
        if not node.is_linked(self.parking):
            if parking_road is None:
                parking_road = Road()
            node.add_node(self.parking, parking_road)

        self.warehouses.append(node)

    def add_consumer(self, node: Consumer):
        self.consumers.append(node)

    def add_parking(self, node: Parking):
        self.parking = node

    def add_transport(self, truck: Transport):
        self.parking.add_transport(truck)

    def add_link(self, ind1: int, ind2: int, dist=1.0, time=1.0):
        if max(ind1, ind2) >= len(self.nodes) or min(ind1, ind2) < 0 or ind1 == ind2:
            raise Exception('Wrong index')

        obj1 = self.nodes[ind1]
        obj2 = self.nodes[ind2]
        obj1.add_node(obj2, Road(dist, time))

    def unlinked(self, node: GeoNode):
        return list(filter(
            lambda other: not (node.is_linked(other) or node == other),
            self.nodes
        ))

    def del_node(self, key: GeoNode):
        if key == self.parking:
            self.parking = None
        elif key in self.consumers:
            key: Consumer
            self.consumers.remove(key)
        elif key in self.warehouses:
            key: Warehouse
            self.warehouses.remove(key)
        else:
            raise Exception('No such node')

        key.unlink()

    def __delitem__(self, key: Union[GeoNode, int]):
        if isinstance(key, GeoNode):
            self.del_node(key)
        elif isinstance(key, int):
            self.del_node(self.nodes[key])
        else:
            raise Exception('Unexpected type')

    @property
    def transport(self) -> List[Transport]:
        return self.parking.transport

    @property
    def nodes(self) -> List[GeoNode]:
        res = [self.parking] if self.parking is not None else []
        res += self.warehouses
        res += self.consumers
        return res

    @property
    def balance_snapshot(self) -> Dict[GeoNode, Dict[str, int]]:
        snapshot: Dict[GeoNode, Dict[str, int]] = {}
        for node in self.nodes:
            snapshot[node] = copy(node.balance)
        return snapshot

    def balance_rollback(self, snapshot: Dict[GeoNode, Dict[str, int]]):
        for node in self.nodes:
            node.balance = snapshot[node]

    class Loader:
        @staticmethod
        def save(sys: 'TransportSystem', f_name: str):
            with open(f_name, 'w', encoding='utf-8') as f:
                sys.save_json(f)

        @staticmethod
        def load(f_name: str) -> 'TransportSystem':
            with open(f_name, 'r', encoding='utf-8') as f:
                return TransportSystem.load_json(f)
