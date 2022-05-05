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

    def __sub__(self, other: 'ProductList'):
        return self.cross(other)

    def cross(self, other: 'ProductList') -> 'ProductList':
        cross_list = ProductList()
        for product in self:
            stock_prod = other.by_name(product.name)
            if stock_prod:
                cross = Product(product.name, min(product.amount, stock_prod.amount))
                cross_list.append(cross)
        return cross_list
