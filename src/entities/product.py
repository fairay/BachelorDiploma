from typing import Union


class Product:
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

    def __repr__(self) -> str:
        return f'{self.name}: {self.amount}'


class ProductList(list[Product]):
    def by_name(self, name: str) -> Product | None:
        found = list(filter(lambda node: node.name == name, self))
        return found[0] if found else None

    def __mul__(self, other: 'ProductList') -> 'ProductList':
        return self.cross(other)

    def cross(self, other: 'ProductList') -> 'ProductList':
        cross_list = ProductList()
        for product in self:
            stock_prod = other.by_name(product.name)
            if stock_prod:
                cross = Product(product.name, min(product.amount, stock_prod.amount))
                cross_list.append(cross)
        return cross_list

    def minus(self, other: 'ProductList'):
        for product in other:
            self_prod = self.by_name(product.name)
            if not self_prod:
                continue

            if self_prod.amount == product.amount:
                self.remove(self_prod)
            else:
                self_prod.amount -= product.amount

    def is_empty(self):
        return len(self) == 0

    def volume(self, prod_vol: float = 1.0):
        return sum(prod.amount for prod in self) * prod_vol
