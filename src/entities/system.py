from typing import List, Optional, Union, TextIO

import jsonpickle

from entities.nodes import Warehouse, Parking, Consumer
from entities.nodes.geonode import GeoNode
from entities.road import Road
from entities.route import Route
from entities.transport import Transport


class TransportSystem(object):
    def __init__(self):
        self.transport: List[Transport] = []
        self.routes: List[Route] = []

        self.parking: Optional[Parking] = None
        self.warehouses: List[Warehouse] = []
        self.consumers: List[Consumer] = []

        self.vol: float = 1.0
        self.con: float = 1.0

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

    def check_valid(self) -> None:
        if self.parking is None:
            raise Exception("No parking")

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
        self.transport = self.parking.transport

    def add_transport(self, truck: Transport):
        self.transport.append(truck)

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

    def _get_nodes(self) -> List[GeoNode]:
        res = [self.parking] if self.parking is not None else []
        res += self.warehouses
        res += self.consumers
        return res

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

    nodes = property(_get_nodes)

    class Loader:
        @staticmethod
        def save(sys: 'TransportSystem', f_name: str):
            with open(f_name, 'w', encoding='utf-8') as f:
                sys.save_json(f)

        @staticmethod
        def load(f_name: str) -> 'TransportSystem':
            with open(f_name, 'r', encoding='utf-8') as f:
                return TransportSystem.load_json(f)
