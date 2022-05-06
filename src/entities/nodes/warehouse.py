from copy import copy

from .geonode import GeoNode
from ..product import ProductList, Product


class Warehouse(GeoNode):
    stock: ProductList
    rest: ProductList

    def __init__(self, name="Склад", *stock: Product):
        super().__init__(name)
        self.stock = ProductList(stock)
        self.rest = ProductList()

    def __copy__(self) -> 'Warehouse':
        new = Warehouse(self.name, *self.stock)
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

        self.stock = ProductList()
        for product in other.stock:
            self.add_product(product)
