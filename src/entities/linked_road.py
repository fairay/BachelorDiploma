from .nodes import GeoNode
from .road import Road


class LinkedRoad(Road):
    def __init__(self, node1: GeoNode, node2: GeoNode, dist=1.0, time=1.0):
        super(LinkedRoad, self).__init__(dist, time)
        self.node1 = node1
        self.node2 = node2
