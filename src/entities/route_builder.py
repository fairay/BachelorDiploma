from copy import copy
from typing import List, Dict

from . import Product
from .geonode import Warehouse, Consumer
from .route import Route
from .system import TransportSystem


def collect_products(*node_products: List[Product]) -> List[Product]:
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
    all_stocks: List[Product]
    all_orders: List[Product]

    stocks: Dict[Warehouse, List[Product]]
    orders: Dict[Consumer, List[Product]]

    def __init__(self, sys: TransportSystem):
        self.sys = sys
        self.init_orders()

    def init_orders(self):
        self.all_stocks = collect_products(*[node.stock for node in self.sys.warehouses])
        self.all_orders = collect_products(*[node.order for node in self.sys.consumers])
        if not enough_products(self.all_stocks, self.all_orders):
            raise Exception('Orders have more products, than stocks are storing')

        self.stocks = {w_node: collect_products(w_node.stock) for w_node in self.sys.warehouses}
        self.orders = {c_node: collect_products(c_node.order) for c_node in self.sys.consumers}

    def calc_routes(self) -> List[Route]:
        routes = self._init_routes()
        routes = self._main_routes(routes)
        return routes

    def _init_routes(self) -> List[Route]:

        for c_node in self.sys.consumers:
            c_node.linked

        return []

    def _main_routes(self, pre_routes: List[Route]) -> List[Route]:
        return []
