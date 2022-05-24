import random
from copy import copy
from random import shuffle
from typing import Dict

import networkx as nx
from scipy.spatial.distance import euclidean

from entities import TransportSystem, Parking, Product, Warehouse, Consumer, Transport

DISC_SCALE = 10.0
MIN_SPEED = 0.5
MAX_SPEED = 1.0
TRUCK_N = 10


def random_system(node_n: int, warehouse_n: int) -> TransportSystem:
    random.seed(2)
    G = nx.random_geometric_graph(node_n, 0.2, seed=1)
    trans = list(range(node_n))
    shuffle(trans)

    sys = TransportSystem()
    sys.vol = 0.1
    sys.con = 5.0

    sys.add_parking(Parking())

    prod = Product('пряники', 10)
    for i in range(warehouse_n):
        w = Warehouse(f'С {i}')
        prod = Product('пряники', random.randint(14 * node_n // warehouse_n, 160 * node_n // warehouse_n))
        w.add_product(prod)
        sys.add_warehouse(w)

    for i in range(node_n - 1 - warehouse_n):
        c = Consumer(f'П {i}')
        prod.amount = random.randint(8, 10)
        c.add_product(prod)
        sys.add_consumer(c)

    for i in range(TRUCK_N):
        sys.add_transport(Transport('Нива'))

    for edge in G.edges:
        ind0, ind1 = trans[edge[0]], trans[edge[1]]
        node0, node1 = G.nodes[ind0], G.nodes[ind1]
        pos0, pos1 = node0['pos'], node1['pos']
        dist = euclidean(pos0, pos1) * DISC_SCALE
        time = dist / (MIN_SPEED + random.random() * (MAX_SPEED - MIN_SPEED))
        sys.add_link(ind0, ind1, dist, time)

    to_delete = []
    for cnode in sys.consumers:
        cnt = len(list(filter(lambda n: isinstance(n, Warehouse), cnode.linked)))
        if not cnt:
            to_delete.append(cnode)

    # for cnode in to_delete:
    #     sys.del_node(cnode)

    return sys


def init_transport() -> Dict[Transport, int]:
    return {
        Transport("ГАЗель NEXT", 13.500, 10.0): 3,
        Transport('Ford Transit', 5.190, 10.0): 0,  # V - 4200-15100
        Transport('ГАЗель Бизнес', 9.000, 10.0): 0,  # V - 9000-11000

        Transport("LADA Largus универсал", 2.350, 10.0): 0,
        Transport("УАЗ 3909 Комби", 2.693, 10.0): 0,
        Transport('ГАЗ-2752 «Соболь Бизнес»', 6.860, 10.0): 0,

        Transport('УАЗ «Профи»', 7.200, 10.0): 0,
        Transport('ГАЗ-3221', 8.370, 10.0): 0,  # V - ?
        Transport('УАЗ-2206', 2.000, 10.0): 0,  # V - ???

        Transport('Hyundai Starex (H-1)', 4.400, 10.0): 0,
    }


def init_parking() -> Parking:
    p = Parking()

    transport = init_transport()
    for truck, amount in transport.items():
        for _ in range(amount):
            p.add_transport(copy(truck))

    return p


def init_system():
    tsys = TransportSystem()

    tsys.add_parking(init_parking())

    tsys.add_warehouse(Warehouse("Склад №1", Product('шоколад', 10)))
    tsys.add_warehouse(Warehouse("Склад №2", Product('кола', 10), Product('кофе', 20)))
    tsys.add_warehouse(Warehouse("Склад №3", Product('кола', 10), Product('шоколад', 20)))

    tsys.add_consumer(Consumer("Потребитель №1", Product('кола', 15), Product('шоколад', 10)))
    tsys.add_consumer(Consumer("Потребитель №2", Product('кола', 3), Product('шоколад', 5), Product('кофе', 10)))
    tsys.add_consumer(Consumer("Потребитель №3", Product('шоколад', 5)))

    tsys.add_link(0, 1)
    tsys.add_link(0, 2)
    tsys.add_link(0, 3)

    tsys.add_link(1, 2)
    tsys.add_link(4, 3)
    tsys.add_link(5, 1)
    tsys.add_link(5, 2)
    tsys.add_link(6, 1)

    return tsys
