from copy import copy
from typing import List, Dict

from .nodes import Warehouse, Consumer
from .product import ProductList
from .route import Route
from .system import TransportSystem


def collect_products(*node_products: ProductList) -> ProductList:
    collapsed_arr = ProductList()
    for products in node_products:
        for prod in products:
            old_prod = list(filter(lambda p: p.name == prod.name, collapsed_arr))
            if old_prod:
                old_prod[0] += prod
            else:
                collapsed_arr.append(copy(prod))
    return collapsed_arr


def enough_products(stock: ProductList, order: ProductList) -> bool:
    for prod in order:
        stock_prods = stock.by_name(prod.name)
        if stock_prods is None or stock_prods.amount < prod.amount:
            return False
    return True


class RouteBuilder(object):
    sys: TransportSystem
    all_stocks: ProductList
    all_orders: ProductList

    stocks: Dict[Warehouse, ProductList]
    orders: Dict[Consumer, ProductList]

    def __init__(self, sys: TransportSystem):
        self.sys = sys
        sys.check_valid()
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
        all_routes: List[Route] = []
        for c_node in self.sys.consumers:
            for w_node in c_node.linked:
                if not isinstance(w_node, Warehouse):
                    continue

                w_node: Warehouse
                route = Route(self.sys.parking, w_node, c_node)
                all_routes.append(route)

        all_routes.sort(key=lambda route: route.dist)

        transport = self.sys.parking.transport

        # for c_node in self.sys.consumers:
        #     for w_node in c_node.linked:
        #         if not isinstance(w_node, Warehouse):
        #             continue
        #
        #         w_node: Warehouse
        #         w_node.

        return []

    def _main_routes(self, pre_routes: List[Route]) -> List[Route]:
        return []
