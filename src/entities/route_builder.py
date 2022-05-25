from collections import defaultdict
from copy import copy, deepcopy
from typing import List, Dict, Tuple

from .nodes import Warehouse, Consumer, GeoNode
from .product import ProductList
from .road_map import RoadMap
from .route import Route, RouteList
from .route_shedule import ScheduleBuilder, RouteScheduleList
from .system import TransportSystem

MAX_ITER = 1_000


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
            if not isinstance(other, Consumer):
                continue
            dist = node.dist(other)
            delta = -node_pot + dist
            if delta < 0:
                self.append((delta, other, node))


class RouteBuilder(object):
    sys: TransportSystem
    road_map: RoadMap
    all_stocks: ProductList
    all_orders: ProductList

    stocks: Dict[Warehouse, ProductList]
    orders: Dict[Consumer, ProductList]

    prod_nodes: Dict[str, List[GeoNode]]

    def __init__(self, sys: TransportSystem):
        self.sys = sys
        self.road_map = RoadMap(sys)

        sys.check_valid()
        self.init_orders()

    def init_orders(self):
        self.all_stocks = collect_products(*[node.stock for node in self.sys.warehouses])
        self.all_orders = collect_products(*[node.order for node in self.sys.consumers])
        if not enough_products(self.all_stocks, self.all_orders):
            raise Exception('Orders have more products, than stocks are storing')

        self.stocks = {w_node: collect_products(w_node.stock) for w_node in self.sys.warehouses}
        self.orders = {c_node: collect_products(c_node.order) for c_node in self.sys.consumers}

    def calc_routes(self, iter_limit: int = MAX_ITER) -> RouteScheduleList:
        routes = self._min_elem_routes()
        self.sys.init_balance(routes)

        routes = self._potential_optimize(routes, iter_limit)

        routes = self._close_routes(routes)
        schedule = ScheduleBuilder(self.sys).build_schedule(routes)

        return schedule

    def stat_calc_routes(self) -> (RouteScheduleList, List):
        routes = self._min_elem_routes()
        self.sys.init_balance(routes)

        self._product_dict()
        stat_list = []

        avg_dist = sum(r.dist for r in routes) / len(routes)
        avg_full = sum(r.occupancy for r in routes) / len(routes)
        avg_parking_dist = sum(dist[1].dist for dist in self.road_map.routes[self.sys.parking].items())
        stat_list.append({'cost': routes.cost, 'len': len(routes),
                          'avg_dist': avg_dist, 'avg_full': avg_full, 'avg_parking_dist': avg_parking_dist})

        for i in range(MAX_ITER):
            upd = self._optimization_iteration(routes)

            avg_dist = sum(r.dist for r in routes) / len(routes)
            avg_full = sum(r.occupancy for r in routes) / len(routes)
            stat_list.append({'cost': routes.cost, 'len': len(routes), 'avg_dist': avg_dist, 'avg_full': avg_full})

            if not upd:
                break
            print(f'{i} iter')

        routes = self._close_routes(routes)
        schedule = ScheduleBuilder(self.sys).build_schedule(routes)

        return schedule, stat_list

    def _init_routes(self) -> RouteList:
        self.road_map.find_routes(self.sys.parking)

        all_routes = RouteList()
        for c_node in self.sys.consumers:
            for w_node in c_node.linked:
                if not isinstance(w_node, Warehouse):
                    continue

                w_node: Warehouse
                route = copy(self.road_map.route(self.sys.parking, w_node))
                route.prolong(Route(w_node, c_node))
                all_routes.append(route)

        all_routes.sort(key=lambda route: route.dist)
        return all_routes

    def _distribute_products(self, all_routes: RouteList):
        transport = self.sys.transport
        routes = RouteList()

        for index, r in enumerate(all_routes):
            c_node: Consumer = r.ctail
            w_node: Warehouse = r.find_warehouse(empty_route=True)

            stock = self.stocks[w_node]
            order = self.orders[c_node]
            cross_products = order * stock
            if cross_products.is_empty():
                continue

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

    def _init_long_routes(self, target_nodes: List[Consumer]) -> RouteList:
        self.road_map.find_routes(self.sys.parking)

        all_routes = RouteList()
        for c_node in target_nodes:
            for w_node in self.sys.warehouses:
                if w_node.is_linked(c_node):
                    continue
                route_w = copy(self.road_map.route(self.sys.parking, w_node))
                route_c = copy(self.road_map.route(w_node, c_node))
                route_w.prolong(route_c)
                all_routes.append(route_w)

        all_routes.sort(key=lambda route: route.dist)
        return all_routes

    def _min_elem_routes(self) -> RouteList:
        all_routes = self._init_routes()
        routes = self._distribute_products(all_routes)

        unsatisfied = list(filter(lambda c: not self.orders[c].is_empty(), self.sys.consumers))
        if len(unsatisfied):
            long_routes = self._init_long_routes(unsatisfied)
            routes += self._distribute_products(long_routes)

        return routes

    def _optimization_iteration(self, pre_routes: RouteList) -> bool:
        pot = self._calculate_potentials(pre_routes)
        disc = self._calculate_discrepancy(pot, pre_routes)
        merged_disc = self._merge_discrepancy(disc)
        pending_routes = pre_routes.blank_routes

        balance_snapshot = self.sys.balance_snapshot
        init_cost = pre_routes.cost

        viewed_nodes: Dict[GeoNode, List[Route]] = defaultdict(lambda: [])
        for from_node in self.sys.consumers:
            from_routes = pending_routes.by_tail(from_node).sort_occupancy
            for to_node in from_node.linked:
                if isinstance(to_node, Consumer):
                    viewed_nodes[to_node] += from_routes

        for local_disc, from_node, to_node in merged_disc:
            to_routes = pending_routes.by_tail(to_node).sort_occupancy
            alt_routes = sorted(viewed_nodes[to_node], key=lambda r: r.tail.dist(to_node) * r.occupancy)

            for route in to_routes:
                route_snapshot = pre_routes.snapshot
                upd_routes = RouteList([route])

                for alt_route in alt_routes:
                    upd_routes.append(alt_route)
                    if alt_route.take_over(route):
                        new_view = [alt_route] + viewed_nodes[route.tail]
                        alt_routes = sorted(filter(lambda r: r.tail.dist(route.tail), new_view),
                                            key=lambda r: r.tail.dist(route.tail) * r.occupancy)

                    if route.warehouse is None:
                        if pre_routes.cost - route.cost * 2 <= init_cost:
                            pre_routes.remove(route)
                            return True
                        else:
                            break

                    new_cost = pre_routes.cost
                    if new_cost < init_cost:
                        return True
                    elif new_cost - route.cost > init_cost:
                        break

                self.sys.balance_rollback(balance_snapshot)
                upd_routes.rollback(route_snapshot)

        return False

    def _potential_optimize(self, pre_routes: RouteList, iter_limit: int = MAX_ITER) -> RouteList:
        if not iter_limit:
            return pre_routes

        self._product_dict()

        for i in range(iter_limit):
            upd = self._optimization_iteration(pre_routes)
            if not upd:
                break
            print(f'{i} optimization stage done')
        else:
            print(f'Iteration limit {MAX_ITER} reached')

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

    def _calculate_discrepancy(self, pot: Dict[str, ProductPot], routes: RouteList) -> Dict[str, ProductDisc]:
        disc: Dict[str, ProductDisc] = {prod: ProductDisc(prod, prod_pot, routes) for prod, prod_pot in pot.items()}
        return disc

    def _merge_discrepancy(self, disc: Dict[str, ProductDisc]) -> List[Tuple[float, GeoNode, GeoNode]]:
        prod_min: Dict[GeoNode, Tuple[float, GeoNode, GeoNode]] = defaultdict(lambda: (1e10, None, None))
        # merged_disc: List[Tuple[float, GeoNode, GeoNode]] = []
        for prod, prod_disc in disc.items():
            for val in prod_disc:
                if val[0] < prod_min[val[2]][0]:
                    prod_min[val[2]] = val
            # merged_disc += prod_disc

        merged_disc = [val for val in prod_min.values()]

        merged_disc.sort(key=lambda x: x[0])
        return merged_disc

    def _close_routes(self, routes: RouteList) -> RouteList:
        self.road_map.find_routes(self.sys.parking)

        for route in routes:
            route_back = self.road_map.route(route.tail, self.sys.parking)
            route.prolong(route_back)

        return routes
