from copy import copy
from typing import List

from .geonode import Product
from .route import Route
from .system import TransportSystem


def collect_products(node_products: List[List[Product]]) -> List[Product]:
    collapsed_arr: List[Product] = []
    for products in node_products:
        for prod in products:
            old_prod = list(filter(lambda p: p.name == prod.name, collapsed_arr))
            if old_prod:
                old_prod[0] += prod
            else:
                collapsed_arr.append(copy(prod))
    return collapsed_arr


def enough_products(stock: List[Product], order: List[Product]):
    for prod in order:
        stock_prods = list(filter(lambda p: p.name == prod.name, stock))
        if not stock_prods:
            return False
        elif stock_prods[0].amount < prod.amount:
            return False
    return True


class RouteBuilder(object):
    sys: TransportSystem

    def __init__(self, sys: TransportSystem):
        self.sys = sys
        self.stocks: List[Product] = collect_products([node.stock for node in sys.warehouses])
        self.orders: List[Product] = collect_products([node.order for node in sys.consumers])
        if not enough_products(self.stocks, self.orders):
            raise Exception('Orders have more products, than stocks are storing')

    def init_orders(self):
        pass

    def calc_routes(self) -> List[Route]:
        routes = self._init_routes()
        routes = self._main_routes(routes)
        return routes

    def _init_routes(self) -> List[Route]:
        return []

    def _main_routes(self, pre_routes: List[Route]) -> List[Route]:
        return []
