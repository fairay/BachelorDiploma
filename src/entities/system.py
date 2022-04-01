from typing import List, Optional

from entities.geonode import Parking, Warehouse, Consumer, GeoNode
from entities.transport import Transport, Route


class TransportSystem:
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
        if max(ind1, ind2) >= len(self.node_arr) or min(ind1, ind2) < 0 or ind1 == ind2:
            raise Exception('Wrong index')

        obj1 = self.node_arr[ind1]
        obj2 = self.node_arr[ind2]
        obj1.add_node(obj2, dist, time)
        obj2.add_node(obj1, dist, time)

    def unlinked(self, node: GeoNode):
        return list(filter(
            lambda other: not (node.is_linked(other) or node == other),
            self.node_arr
        ))

    def calc_routes(self):
        self._init_routes()
        self._main_routes()

    def _init_routes(self):
        path_len = []
        # for node in self.warehouses:

    def _main_routes(self):
        pass

    def _get_nodes(self) -> List[GeoNode]:
        res = [self.parking] if self.parking is not None else []
        res += self.warehouses
        res += self.consumers
        return res

    node_arr = property(_get_nodes)