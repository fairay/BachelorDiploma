from typing import List, Optional, Dict


class Transport:
    def __init__(self):
        self.volume: float = 0
        self.cons: float = 0


class GeoNode:
    def __init__(self, name=""):
        self.name: str = name

    def __str__(self):
        return self.name


class Warehouse(GeoNode):
    def __init__(self, stock: Dict[str, int]):
        super().__init__()
        self.stock = stock


class Parking(GeoNode):
    def __init__(self):
        super(Parking, self).__init__('Стоянка')


class Consumer(GeoNode):
    def __init__(self, order: Dict[str, int]):
        super().__init__()
        self.order = order


class Route:
    def __init__(self, parking: Parking):
        self.nodes: List[GeoNode] = [parking]


class TransportSystem:
    def __init__(self):
        self.nodes: List[GeoNode] = []
        self.transport: List[Transport] = []
        self.routes: List[Route] = []

        self.parking: Optional[Parking] = None
        self.warehouses: List[Warehouse] = []
        self.consumers: List[Consumer] = []

        self.vol: float = 1.0
        self.con: float = 1.0

    def add_warehouse(self, node: Warehouse):
        self.warehouses.append(node)
        self.nodes.append(node)

    def add_consumer(self, node: Consumer):
        self.consumers.append(node)
        self.nodes.append(node)

    def add_parking(self, node: Parking):
        if self.parking:
            self.nodes.remove(self.parking)

        self.parking = node
        self.nodes.append(node)

    def calc_routes(self):
        self._init_routes()
        self._main_routes()

    def _init_routes(self):
        pass

    def _main_routes(self):
        pass
