from typing import List

from entities import Parking, GeoNode


class Route:
    def __init__(self, parking: Parking):
        self.nodes: List[GeoNode] = [parking]