import sys

import ui.styles as st
from interface import *
from interface import MainWin
from system_generator import random_system


def main(tsys: TransportSystem):
    app = QtWidgets.QApplication([])
    application = MainWin(tsys=tsys)
    application.show()

    app.setStyleSheet(st.stylesheet)
    application.setStyleSheet(st.stylesheet)

    sys.exit(app.exec())


if __name__ == '__main__':
    tsys = None # random_system(100, 10, radius=0.2)
    # TransportSystem.Loader.save(tsys, './configs/rnd100.json')
    # route_builder = RouteBuilder(init_system())
    # routes = route_builder.calc_routes()
    main(tsys)
