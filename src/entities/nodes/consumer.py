from copy import copy

from .geonode import GeoNode
from ..product import ProductList, Product


class Consumer(GeoNode):
    order: ProductList
    rest: ProductList

    def __init__(self, order: ProductList, name='Потребитель'):
        super().__init__(name)
        self.order = order
        self.rest = ProductList()

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
