from typing import List, Optional, Dict


class GeoNode(object):
    def __init__(self, name=""):
        self.name: str = name
        self.linked: Dict[GeoNode, Dict[str, float]] = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.name == other.name

    def __hash__(self):
        return id(self)

    def dist(self, other):
        return self.linked[other]['dist'] if self.is_linked(other) else None

    def time(self, other):
        return self.linked[other]['time'] if self.is_linked(other) else None

    def add_node(self, other, dist=1.0, time=1.0, symmetric=True):
        self.linked[other] = {'dist': dist, 'time': time}
        if symmetric:
            other.linked[self] = {'dist': dist, 'time': time}

    def delete_node(self, other, symmetric=True):
        self.linked.pop(other)
        if symmetric:
            other.linked.pop(self)

    def is_linked(self, other):
        return other in self.linked.keys()


class Warehouse(GeoNode):
    def __init__(self, stock: Dict[str, int], name=""):
        super().__init__(name)
        self.stock = stock


class Parking(GeoNode):
    def __init__(self):
        super(Parking, self).__init__('Стоянка')


class Consumer(GeoNode):
    def __init__(self, order: Dict[str, int]):
        super().__init__()
        self.order = order
