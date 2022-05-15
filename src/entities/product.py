from typing import Union, Optional


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

    def volume(self, prod_vol: float = 1.0):
        return self.amount * prod_vol

    def split(self, new_amount: int) -> Optional['Product']:
        if new_amount >= self.amount:
            return None

        rem = Product(self.name, self.amount - new_amount)
        self.amount -= new_amount
        return rem

    def to_restriction(self, volume: float, prod_vol: float = 1.0) -> Optional['Product']:
        new_amount = int(volume / prod_vol)
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

    def volume(self, prod_vol: float = 1.0) -> float:
        return sum(prod.volume(prod_vol) for prod in self)

    def to_restriction(self, volume: float, prod_vol: float = 1.0) -> 'ProductList':
        """
        Restricts list to fit given volume

        Returns reminder list of products
        """

        if self.volume(prod_vol) <= volume:
            return ProductList()

        rem = ProductList(self)
        rem.sort(key=lambda prod: prod.amount, reverse=True)
        self.clear()

        self_vol = 0
        for prod in rem:
            prod_vol = prod.volume(prod_vol)
            if self_vol + prod_vol < volume:
                self.append(prod)
                self_vol += prod_vol
        rem.minus(self)

        if self_vol < volume * 0.99:
            prod = rem[0].to_restriction(volume - self_vol, prod_vol)
            self.append(rem[0])
            rem[0] = prod

        return rem
