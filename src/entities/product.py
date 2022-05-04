from typing import Union, List


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

    def cross(self, stock: List['Product'], order: List['Product']):
        cross_list = []
        return cross_list


class ProductList(list):
    def by_name(self, name: str) -> Product | None:
        found = list(filter(lambda node: node.name == name, self))
        return found[0] if found else None
