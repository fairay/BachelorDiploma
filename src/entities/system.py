from typing import List, Optional, Union

from entities.geonode import Parking, Warehouse, Consumer, GeoNode
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

    def add_warehouse(self, node: Warehouse):
        self.warehouses.append(node)

    def add_consumer(self, node: Consumer):
        self.consumers.append(node)

    def add_parking(self, node: Parking):
        self.parking = node

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
