import queue
from typing import Dict, Tuple

from .nodes import GeoNode
from .route import Route
from .system import TransportSystem


class RoadMap():
    sys: TransportSystem
    routes: Dict[GeoNode, Dict[GeoNode, Route]]
    dists: Dict[GeoNode, Dict[GeoNode, float]]

    def __init__(self, sys: TransportSystem):
        self.sys = sys
        self.routes = {}
        self.dists = {}

    def find_routes(self, node: GeoNode):
        if node in self.routes:
            return

        self.routes[node] = {}
        self.dists[node] = {}

        q: queue.Queue[Tuple[float, Route]] = queue.Queue()
        q.put((0, Route(node)))

        while not q.empty():
            dist, route = q.get()
            current = route.tail

            if self.dists[node].get(current, 1e+100) <= dist:
                continue

            self.dists[node][current] = dist
            self.routes[node][current] = route

            for other in current.linked:
                other_dist = dist + current.dist(other)

                if self.dists[node].get(other, 1e+100) > other_dist:
                    other_route = route.extend(other)
                    q.put((other_dist, other_route))

    def route(self, from_node: GeoNode, to_node: GeoNode) -> Route:
        if from_node in self.routes:
            return self.routes[from_node][to_node]
        elif from_node in self.routes[to_node]:
            return self.routes[to_node][from_node].inverse()
        else:
            self.find_routes(from_node)
            return self.routes[from_node][to_node]
