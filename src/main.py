import sys
from typing import Type

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QListWidgetItem
import plotly

from transport import *
from interface import *
from graphics import get_figure
from ui.node_dialog import NodeDialog

from ui.node_list import WarehouseField, ListField


def main():
    trans = TransportSystem()

    p = Parking()
    trans.add_parking(p)

    ware = [Warehouse({'Сникерс': 40, 'Хлеб': 10})]
    p.add_node(ware[0], 2.4, 5.0)
    trans.add_warehouse(ware[0])

    cons = [Consumer({'Сникерс': 20}), Consumer({'Сникерс': 10, 'Хлеб': 5})]
    ware[0].add_node(cons[0], 5.0, 15.0)
    ware[0].add_node(cons[1], 7.0, 20.0)
    trans.add_consumer(cons[0])
    trans.add_consumer(cons[1])


class MainWin(QtWidgets.QMainWindow):
    ui = None

    def __init__(self):
        super().__init__()
        self.ui = GuiMainWin()
        self.ui.setupUi(self)

        self.sys = TransportSystem()

        self.setAnimated(True)
        self.setUpdatesEnabled(True)
        self.build_figure()
        self.fill_list()

    def build_figure(self):
        fig = get_figure()
        html = '<html><body>'
        html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')
        html += '</body></html>'
        plot_widget = QWebEngineView()
        plot_widget.setHtml(html)
        self.ui.GraphWidget.addWidget(plot_widget)

    def show_node(self, widget: ListField):
        item = QListWidgetItem(self.ui.NodeList)
        item.setSizeHint(widget.sizeHint())
        self.ui.NodeList.addItem(item)
        self.ui.NodeList.setItemWidget(item, widget)

    def fill_list(self):
        node = Warehouse({}, "Склад №1")
        self.sys.add_warehouse(node)
        self.show_node(WarehouseField(node, self.show_dialog))

        node = Warehouse({}, "Склад №2")
        self.sys.add_warehouse(node)
        self.sys.add_link(0, 1)
        self.show_node(WarehouseField(node, self.show_dialog))


    def show_dialog(self, dialog: Type[NodeDialog], node: GeoNode):
        form = dialog(node, self.sys)
        form.exec_()


if __name__ == '__main__':
    main()
    global app, application
    app = QtWidgets.QApplication([])
    application = MainWin()
    application.show()

    sys.exit(app.exec())
