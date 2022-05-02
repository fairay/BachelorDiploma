from entities import Road, GeoNode


class LinkedRoad(Road):
    def __init__(self, node1: GeoNode, node2: GeoNode, dist=1.0, time=1.0):
        super(LinkedRoad, self).__init__(dist, time)
        self.node1 = node1
        self.node2 = node2

        # node1.add_node(node2)

    def __del__(self):
        self.node1.delete_node(self.node2, symmetric=False)
        self.node2.delete_node(self.node1, symmetric=False)
