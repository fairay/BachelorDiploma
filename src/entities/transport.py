from geonode import *


class Transport:
    def __init__(self):
        self.volume: float = 0
        self.cons: float = 0


class Route:
    def __init__(self, parking: Parking):
        self.nodes: List[GeoNode] = [parking]


