from copy import copy
from typing import *

from ..road import Road


class GeoNode(object):
    def __init__(self, name=""):
        self.name: str = name
        self.linked: Dict[GeoNode, Road] = {}
        self.balance: Dict[str, int] = {}

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
        return self.linked[other].dist if self.is_linked(other) else None

    def time(self, other: 'GeoNode'):
        return self.linked[other].time if self.is_linked(other) else None

    def add_node(self, other: 'GeoNode', road: Road, symmetric=True):
        self.linked[other] = road
        if symmetric:
            other.add_node(self, road, symmetric=False)

    def delete_node(self, other: 'GeoNode', symmetric=True):
        if not self.is_linked(other):
            return
        self.linked.pop(other)
        if symmetric:
            other.delete_node(self, symmetric=False)

    def unlink(self):
        keys = self.linked.keys()
        for other in list(keys):
            self.delete_node(other)

    def is_linked(self, other: 'GeoNode'):
        return other in self.linked.keys()

    def update(self, other: 'GeoNode'):
        self.name = other.name
        self.unlink()
        for node, road in other.linked.items():
            self.add_node(node, road)
