from copy import copy
from typing import *

from .transport import Transport


class GeoNode(object):
    def __init__(self, name=""):
        self.name: str = name
        self.linked: Dict[GeoNode, Dict[str, float]] = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other: 'GeoNode'):
        return isinstance(other, type(self)) and self.name == other.name

    def __hash__(self):
        return id(self)

    def __copy__(self) -> 'GeoNode':
        new = GeoNode(self.name)
        new.linked = copy(self.linked)
        return new

    def dist(self, other: 'GeoNode'):
        return self.linked[other]['dist'] if self.is_linked(other) else None

    def time(self, other: 'GeoNode'):
        return self.linked[other]['time'] if self.is_linked(other) else None

    def add_node(self, other: 'GeoNode', dist=1.0, time=1.0, symmetric=True):
        self.linked[other] = {'dist': dist, 'time': time}
        if symmetric:
            other.linked[self] = {'dist': dist, 'time': time}

    def delete_node(self, other: 'GeoNode', symmetric=True):
        if not self.is_linked(other):
            return
        self.linked.pop(other)
        if symmetric:
            other.delete_node(self, False)

    def unlink(self):
        keys = self.linked.keys()
        for other in list(keys):
            self.delete_node(other)

    def is_linked(self, other: 'GeoNode'):
        return other in self.linked.keys()

    def update(self, other: 'GeoNode'):
        self.name = other.name
        self.unlink()
        for node, data in other.linked.items():
            self.add_node(node, **data)


class Warehouse(GeoNode):
    def __init__(self, stock: Dict[str, int], name=""):
        super().__init__(name)
        self.stock = stock


class Parking(GeoNode):
    def __init__(self, name='Стоянка'):
        super(Parking, self).__init__(name)
        self.transport: List[Transport] = []

    def __copy__(self) -> 'Parking':
        new = Parking(self.name)
        new.linked = copy(self.linked)
        new.transport = copy(self.transport)
        return new

    def add_transport(self, track: Transport):
        for i, t in enumerate(self.transport):
            if track.name == t.name:
                self.transport[i] = track
                return

        self.transport.append(track)

    def update(self, other: 'Parking'):
        super(Parking, self).update(other)

        for track in other.transport:
            self.add_transport(track)


class Consumer(GeoNode):
    def __init__(self, order: Dict[str, int], name='Потребитель'):
        super().__init__(name)
        self.order = order
