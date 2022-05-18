from copy import copy
from typing import List, Dict

from .nodes import Warehouse, Consumer, GeoNode
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

    prod_nodes: Dict[str, List[GeoNode]]
    pot: Dict[str, Dict[GeoNode, float]]

    def __init__(self, sys: TransportSystem):
        self.sys = sys
        self.pot = {}

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
        routes = self._estimate_routes()
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
        return all_routes

    def _estimate_routes(self) -> List[Route]:
        all_routes = self._init_routes()

        transport = self.sys.parking.transport
        routes = []

        for index, r in enumerate(all_routes):
            c_node: Consumer = r.nodes[-1]
            w_node: Warehouse = r.nodes[-2]

            stock = self.stocks[w_node]
            order = self.orders[c_node]
            if stock.is_empty() or order.is_empty():
                continue

            cross_products = order * stock
            selected_track = transport[index % len(transport)]

            stock.minus(cross_products)
            order.minus(cross_products)
            r.set_track(selected_track)
            r.set_load(w_node, cross_products)
            r.set_load(c_node, cross_products)
            routes.append(r)

        return routes

    def _main_routes(self, pre_routes: List[Route]) -> List[Route]:
        self._product_dict()
        self._calculate_potentials(pre_routes)

        return pre_routes

    def _product_dict(self):
        self.prod_nodes = {}

        for wnode in self.sys.warehouses:
            for prod in wnode.stock:
                if prod.name in self.prod_nodes.keys():
                    self.prod_nodes[prod.name].append(wnode)
                else:
                    self.prod_nodes[prod.name] = [wnode]

        for cnode in self.sys.consumers:
            for prod in cnode.order:
                if prod.name in self.prod_nodes.keys():
                    self.prod_nodes[prod.name].append(cnode)
                else:
                    self.prod_nodes[prod.name] = [cnode]

    def _calculate_potentials(self, routes: List[Route]):
        self.pot = {}
        print(self.pot)

        for prod in self.prod_nodes.keys():
            self.pot[prod] = {}

        for route in routes:
            prod_names = route.prod_names

            for node, dist in route.node_dist.items():
                for prod in prod_names:
                    self.pot[prod][node] = dist
