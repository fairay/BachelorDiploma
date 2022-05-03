from copy import copy
from typing import *

from .road import Road
from .transport import Transport


class GeoNode(object):
    def __init__(self, name=""):
        self.name: str = name
        self.linked: Dict[GeoNode, Road] = {}

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


class Product(object):
    __match_args__ = ('name',)

    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def __iadd__(self, other: Union['Product', int]):
        match other:
            case Product(name) if name == self.name:
                self.amount += other.amount
            case int():
                self.amount += other
            case _:
                raise Exception('Wrong type for addition')
        return self


class Warehouse(GeoNode):
    def __init__(self, stock: List[Product], name=""):
        super().__init__(name)
        self.stock = stock

    def __copy__(self) -> 'Warehouse':
        new = Warehouse(self.stock, self.name)
        new.linked = copy(self.linked)
        new.stock = copy(self.stock)
        return new

    def del_product(self, product: Product):
        for i, p in enumerate(self.stock):
            if product.name == p.name:
                del self.stock[i]

    def add_product(self, new_product: Product):
        for i, product in enumerate(self.stock):
            if new_product.name == product.name:
                self.stock[i] = new_product
                return

        self.stock.append(new_product)

    def update(self, other: 'Warehouse'):
        super(Warehouse, self).update(other)

        self.stock = []
        for product in other.stock:
            self.add_product(product)


class Parking(GeoNode):
    def __init__(self, name='Стоянка'):
        super(Parking, self).__init__(name)
        self.transport: List[Transport] = []

    def __copy__(self) -> 'Parking':
        new = Parking(self.name)
        new.linked = copy(self.linked)
        new.transport = copy(self.transport)
        return new

    def del_transport(self, track: Transport):
        for i, t in enumerate(self.transport):
            if track.name == t.name:
                del self.transport[i]

    def add_transport(self, track: Transport):
        for i, t in enumerate(self.transport):
            if track.name == t.name:
                self.transport[i] = track
                return

        self.transport.append(track)

    def update(self, other: 'Parking'):
        super(Parking, self).update(other)

        self.transport = []
        for track in other.transport:
            self.add_transport(track)


class Consumer(GeoNode):
    def __init__(self, order: List[Product], name='Потребитель'):
        super().__init__(name)
        self.order: List[Product] = order

    def __copy__(self) -> 'Consumer':
        new = Consumer(self.order, self.name)
        new.linked = copy(self.linked)
        new.order = copy(self.order)
        return new

    def del_product(self, product: Product):
        for i, p in enumerate(self.order):
            if product.name == p.name:
                del self.order[i]

    def add_product(self, new_product: Product):
        for i, product in enumerate(self.order):
            if new_product.name == product.name:
                self.order[i] = new_product
                return

        self.order.append(new_product)

    def update(self, other: 'Consumer'):
        super(Consumer, self).update(other)

        self.order = []
        for product in other.order:
            self.add_product(product)
