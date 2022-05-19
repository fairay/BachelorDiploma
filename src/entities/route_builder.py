from copy import copy, deepcopy
from typing import List, Dict, Tuple

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


class ProductPot(dict[GeoNode, float]):
    def apply_route(self, route: Route):
        for node, dist in route.node_dist.items():
            self[node] = min(self.get(node, dist), dist)


class ProductDisc(List[Tuple[float, GeoNode, GeoNode]]):
    # potential, from, to

    def __init__(self, prod: str, pot: ProductPot, routes: List[Route]):
        super(ProductDisc, self).__init__()

        self.prod = prod
        self.pot = pot

        for node in pot.keys():
            self._process_node(node)

        del self.pot

    def _process_node(self, node: GeoNode):
        if not isinstance(node, Consumer):
            return

        node_pot = self.pot[node]
        for other in node.linked:
            dist = node.dist(other)
            delta = -node_pot + dist
            if delta < 0:
                self.append((delta, other, node))


class RouteBuilder(object):
    sys: TransportSystem
    all_stocks: ProductList
    all_orders: ProductList

    stocks: Dict[Warehouse, ProductList]
    orders: Dict[Consumer, ProductList]

    prod_nodes: Dict[str, List[GeoNode]]

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
        routes = self._estimate_routes()
        self.sys.init_balance(routes)
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
            c_node: Consumer = r.ctail
            w_node: Warehouse = r.find_warehouse(empty_route=True)

            stock = self.stocks[w_node]
            order = self.orders[c_node]
            if stock.is_empty() or order.is_empty():
                continue

            cross_products = order * stock
            selected_track = transport[index % len(transport)]
            if cross_products.volume >= selected_track.volume:
                cross_products.to_restriction(selected_track.volume)
                all_routes.append(copy(r))

            stock.minus(cross_products)
            order.minus(cross_products)
            r.set_track(selected_track)
            r.set_load(w_node, deepcopy(cross_products))
            r.set_load(c_node, deepcopy(cross_products))
            routes.append(r)

        return routes

    def _optimization_iteration(self, pre_routes: List[Route]) -> bool:
        pot = self._calculate_potentials(pre_routes)
        disc = self._calculate_discrepancy(pot, pre_routes)
        merged_disc = self._merge_discrepancy(disc)

        for local_disc, from_node, to_node in merged_disc:

            from_routes: List[Route] = sorted(filter(lambda r: r.tail == from_node, pre_routes),
                                              key=lambda r: r.occupancy)

            to_routes: List[Route] = sorted(filter(lambda r: r.tail == to_node, pre_routes),
                                            key=lambda r: r.occupancy)

            for route in to_routes:
                for alt_route in from_routes:
                    if route.occupancy > 1 - alt_route.occupancy:
                        continue  # not enough space
                    if route.warehouse == alt_route.warehouse:
                        # enough space & same warehouse
                        if alt_route.take_over(route):
                            pre_routes.remove(route)
                            return True

        return False

    def _main_routes(self, pre_routes: List[Route]) -> List[Route]:
        self._product_dict()

        upd = self._optimization_iteration(pre_routes)
        while upd:
            upd = self._optimization_iteration(pre_routes)

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

    def _calculate_potentials(self, routes: List[Route]) -> Dict[str, ProductPot]:
        pot = {prod: ProductPot() for prod in self.prod_nodes.keys()}

        for route in routes:
            for prod in route.prod_names:
                pot[prod].apply_route(route)

        return pot

    def _calculate_discrepancy(self, pot: Dict[str, ProductPot], routes: List[Route]) -> Dict[str, ProductDisc]:
        disc: Dict[str, ProductDisc] = {prod: ProductDisc(prod, prod_pot, routes) for prod, prod_pot in pot.items()}
        return disc

    def _merge_discrepancy(self, disc: Dict[str, ProductDisc]) -> List[Tuple[float, GeoNode, GeoNode]]:
        merged_disc = []
        for prod, prod_disc in disc.items():
            merged_disc += prod_disc

        merged_disc.sort(key=lambda x: x[0])
        return merged_disc
