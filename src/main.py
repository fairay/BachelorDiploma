import sys
from copy import copy
from typing import Dict

import ui.styles as st
from entities import *
from interface import *
from interface import MainWin

a = 10_000


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


def main():
    app = QtWidgets.QApplication([])
    application = MainWin()
    application.show()

    app.setStyleSheet(st.stylesheet)
    application.setStyleSheet(st.stylesheet)

    sys.exit(app.exec())


if __name__ == '__main__':
    # tsys = init_system()
    # TransportSystem.Loader.save(tsys, './configs/data.json')
    # route_builder = RouteBuilder(init_system())
    # routes = route_builder.calc_routes()
    main()
