import sys
from typing import Type, Optional

from PyQt5.QtWidgets import QListWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import ui.styles as st
from entities import *
from entities.route_builder import RouteBuilder
from graphics import get_figure
from interface import *
from interface import GuiMainWin
from ui.dialogs.node import NodeDialog
from ui.node_list import WarehouseField, ListField, ParkingField, ConsumerField


def init_parking() -> Parking:
    p = Parking()
    p.add_transport(Transport("Газель", 10, 10))
    return p


def init_system():
    tsys = TransportSystem()

    tsys.add_parking(init_parking())

    tsys.add_warehouse(Warehouse([Product('шоколад', 10)], "Склад №1"))
    tsys.add_warehouse(Warehouse([Product('кола', 10)], "Склад №2"))
    tsys.add_warehouse(Warehouse([Product('кола', 10), Product('шоколад', 20)], "Склад №3"))

    c = Consumer([Product('кола', 15), Product('шоколад', 35)], "Потребитель №1")
    tsys.add_consumer(c)

    tsys.add_link(0, 1)
    tsys.add_link(0, 2)
    tsys.add_link(0, 3)
    tsys.add_link(1, 2)
    tsys.add_link(4, 3)

    return tsys


class MainWin(QtWidgets.QMainWindow):
    ui: GuiMainWin = None

    def __init__(self, sys: TransportSystem):
        super().__init__()
        self.ui = GuiMainWin()
        self.ui.setupUi(self)
        self.canvas: Optional[FigureCanvasQTAgg] = None

        self.sys = sys

        self.setAnimated(True)
        self.setUpdatesEnabled(True)
        self.build_figure()
        self.render_ui()

    def build_figure(self):
        fig = get_figure(self.sys)

        if self.canvas:
            self.ui.GraphWidget.removeWidget(self.canvas)
        self.canvas = FigureCanvasQTAgg(fig)
        self.ui.GraphWidget.addWidget(self.canvas)

    def clean_list(self):
        self.ui.NodeList.clear()

    def show_node(self, widget: ListField):
        item = QListWidgetItem(self.ui.NodeList)
        item.setSizeHint(widget.sizeHint())
        self.ui.NodeList.addItem(item)
        self.ui.NodeList.setItemWidget(item, widget)

    def render_ui(self):
        self.clean_list()
        if self.sys.parking:
            self.show_node(ParkingField(self.sys.parking, self.show_dialog))

        for wnode in self.sys.warehouses:
            self.show_node(WarehouseField(wnode, self.show_dialog))

        for cnode in self.sys.consumers:
            self.show_node(ConsumerField(cnode, self.show_dialog))

        self.build_figure()

    def show_dialog(self, dialog: Type[NodeDialog], node: GeoNode):
        form = dialog(node, self.sys)
        code = form.exec_()
        if code:
            self.render_ui()


def main():
    app = QtWidgets.QApplication([])
    application = MainWin(init_system())
    application.show()

    app.setStyleSheet(st.stylesheet)
    application.setStyleSheet(st.stylesheet)

    sys.exit(app.exec())


if __name__ == '__main__':
    sys = init_system()
    builder = RouteBuilder(sys)
    main()
