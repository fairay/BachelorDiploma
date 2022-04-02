import sys
from typing import Type

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QListWidgetItem
import plotly

from entities.system import TransportSystem
from entities.transport import *
from interface import *
from graphics import get_figure
from ui.node_dialog import NodeDialog

from ui.node_list import WarehouseField, ListField


def init_system():
    tsys = TransportSystem()

    tsys.add_warehouse(Warehouse({}, "Склад №1"))
    tsys.add_warehouse(Warehouse({}, "Склад №2"))
    tsys.add_warehouse(Warehouse({}, "Склад №3"))

    tsys.add_link(0, 1)
    tsys.add_link(1, 2)

    return tsys

    # p = Parking()
    # trans.add_parking(p)
    #
    # ware = [Warehouse({'Сникерс': 40, 'Хлеб': 10})]
    # p.add_node(ware[0], 2.4, 5.0)
    # trans.add_warehouse(ware[0])
    #
    # cons = [Consumer({'Сникерс': 20}), Consumer({'Сникерс': 10, 'Хлеб': 5})]
    # ware[0].add_node(cons[0], 5.0, 15.0)
    # ware[0].add_node(cons[1], 7.0, 20.0)
    # trans.add_consumer(cons[0])
    # trans.add_consumer(cons[1])


class MainWin(QtWidgets.QMainWindow):
    ui = None

    def __init__(self):
        super().__init__()
        self.ui = GuiMainWin()
        self.ui.setupUi(self)

        self.sys = init_system()

        self.setAnimated(True)
        self.setUpdatesEnabled(True)
        self.build_figure()
        self.update_list()

    def build_figure(self):
        return 
        fig = get_figure()
        html = '<html><body>'
        html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')
        html += '</body></html>'
        plot_widget = QWebEngineView()
        plot_widget.setHtml(html)
        self.ui.GraphWidget.addWidget(plot_widget)

    def clean_list(self):
        self.ui.NodeList.clear()

    def show_node(self, widget: ListField):
        item = QListWidgetItem(self.ui.NodeList)
        item.setSizeHint(widget.sizeHint())
        self.ui.NodeList.addItem(item)
        self.ui.NodeList.setItemWidget(item, widget)

    def update_list(self):
        self.clean_list()
        if self.sys.parking:
            # self.show_node(ParkingField(self.sys.parking, self.show_dialog))
            pass

        for node in self.sys.warehouses:
            self.show_node(WarehouseField(node, self.show_dialog))

        for node in self.sys.consumers:
            # self.show_node(ConsumerField(node, self.show_dialog))
            pass

    def show_dialog(self, dialog: Type[NodeDialog], node: GeoNode):
        form = dialog(node, self.sys)
        form.exec_()

        self.update_list()


def main():
    global app, application

    init_system()
    app = QtWidgets.QApplication([])
    application = MainWin()
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
