from typing import Union, Optional


class Product:
    __match_args__ = ('name',)

    def __init__(self, name: str, amount: int, volume=0.1):
        self.name = name
        self.amount = amount
        self.volume = volume

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

    @property
    def sum_volume(self):
        return self.amount * self.volume

    def split(self, new_amount: int) -> Optional['Product']:
        if new_amount >= self.amount:
            return None

        rem = Product(self.name, self.amount - new_amount, self.volume)
        self.amount = new_amount
        return rem

    def to_restriction(self, volume: float) -> Optional['Product']:
        new_amount = int(volume / self.volume + 1e-4)
        return self.split(new_amount)


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

    @property
    def volume(self) -> float:
        return sum(prod.sum_volume for prod in self)

    @property
    def amount(self) -> int:
        return sum(prod.amount for prod in self)

    def to_restriction(self, volume: float) -> 'ProductList':
        """
        Restricts list to fit given volume

        Returns reminder list of products
        """

        amount = int(volume / self[0].volume + 1e-4)
        if self.volume <= volume:
            return ProductList()

        rem = ProductList(self)
        rem.sort(key=lambda prod: prod.amount, reverse=True)
        self.clear()

        self_amount = 0
        for prod in rem:
            prod_amount = prod.amount
            if self_amount + prod_amount < volume:
                self.append(prod)
                self_amount += prod_amount

        rem.minus(self)

        if self.volume < volume:
            prod = rem[0].split(amount - self_amount)
            self.append(rem[0])
            rem[0] = prod

        return rem
