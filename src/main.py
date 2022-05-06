import sys
from copy import copy
from typing import Type, Dict

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QListWidgetItem, QFileDialog, QShortcut
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

import ui.styles as st
from entities import *
from entities import Product
from entities import RouteBuilder
from graphics import get_figure
from interface import *
from interface import GuiMainWin
from ui.dialogs import ParkingDialog, WarehouseDialog, ConsumerDialog
from ui.dialogs.node import NodeDialog
from ui.node_list import WarehouseField, ListField, ParkingField, ConsumerField

a = 10_000
def init_transport() -> Dict[Transport, int]:
    return {
        Transport("ГАЗель NEXT", 13.500, 10.0): 1,
        Transport('Ford Transit', 5.190, 10.0): 0, # V - 4200-15100
        Transport('ГАЗель Бизнес', 9.000, 10.0): 0, # V - 9000-11000

        Transport("LADA Largus универсал", 2.350, 10.0): 1,
        Transport("УАЗ 3909 Комби", 2.693, 10.0): 1,
        Transport('ГАЗ-2752 «Соболь Бизнес»', 6.860, 10.0): 0,

        Transport('УАЗ «Профи»', 7.200, 10.0): 0,
        Transport('ГАЗ-3221', 8.370, 10.0): 0, # V - ?
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
    tsys.vol = 0.2

    tsys.add_parking(init_parking())

    tsys.add_warehouse(Warehouse("Склад №1", Product('шоколад', 10) ))
    tsys.add_warehouse(Warehouse("Склад №2", Product('кола', 10), Product('кофе', 20)  ))
    tsys.add_warehouse(Warehouse("Склад №3", Product('кола', 10), Product('шоколад', 20) ))

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


class MainWin(QtWidgets.QMainWindow):
    ui: GuiMainWin = None
    window_title = 'Оптимизация маршрутов поставок'

    sys: TransportSystem
    sys_file: str
    unsaved: bool

    def __init__(self, sys_file="configs/data.json", tsys: TransportSystem = None):
        super().__init__()
        self.ui = GuiMainWin()
        self.ui.setupUi(self)
        self.showMaximized()

        self.sys_file = sys_file
        self.unsaved = False
        if tsys:
            self.sys = tsys
        else:
            self.import_sys(sys_file)

        self.render_ui()
        self.set_binds()

    def set_binds(self):
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.export_click)
        self.ui.import_action.triggered.connect(self.import_action)
        self.ui.export_action.triggered.connect(self.export_action)

        self.ui.action_parking.triggered.connect(self.action_parking)
        self.ui.action_warehouse.triggered.connect(self.action_warehouse)
        self.ui.action_consumer.triggered.connect(self.action_consumer)

    def action_parking(self):
        if self.sys.parking:
            self.ui.err_msg("Стоянка уже существует")
            return

        node = Parking()
        self.sys.add_parking(node)
        self.unsaved = True

        self.render_ui()
        self.show_dialog(ParkingDialog, node)

    def action_warehouse(self):
        node = Warehouse()
        self.sys.add_warehouse(node)
        self.unsaved = True

        self.render_ui()
        self.show_dialog(WarehouseDialog, node)

    def action_consumer(self):
        node = Consumer()
        self.sys.add_consumer(node)
        self.unsaved = True

        self.render_ui()
        self.show_dialog(ConsumerDialog, node)

    def import_action(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, 'Выберите конфигурационный файл', './configs/')[0]
            if file_name == '':
                return
            self.import_sys(file_name)

        except Exception as e:
            self.ui.err_msg(str(e))
        self.render_ui()

    def import_sys(self, file_name: str):
        with open(file_name, 'r', encoding='utf-8') as f:
            self.sys = TransportSystem.load_json(f)
        self.sys_file = file_name

    def export_action(self):
        try:
            file_name = QFileDialog.getSaveFileName(self, 'Выберите конфигурационный файл', './configs/')[0]
            if file_name == '':
                return
            self.export_sys(file_name)
        except Exception as e:
            self.ui.err_msg(str(e))

        self.render_ui()

    def export_click(self):
        if not self.unsaved:
            return

        self.export_sys(self.sys_file)
        self.render_ui()

    def export_sys(self, file_name: str):
        with open(file_name, 'w', encoding='utf-8') as f:
            self.sys.save_json(f)
        self.unsaved = False
        self.sys_file = file_name

    def build_figure(self):
        fig = get_figure(self.sys)
        g_layout = self.ui.GraphWidget

        while g_layout.count():
            item = g_layout.itemAt(0)
            g_layout.removeItem(item)
            item.widget().hide()

        canvas = FigureCanvasQTAgg(fig)
        navbar = NavigationToolbar2QT(canvas, None, coordinates=False)

        g_layout.addWidget(canvas)
        g_layout.addWidget(navbar)

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
        for w_node in self.sys.warehouses:
            self.show_node(WarehouseField(w_node, self.show_dialog))
        for c_node in self.sys.consumers:
            self.show_node(ConsumerField(c_node, self.show_dialog))

        self.build_figure()

        self.setWindowTitle(f'{self.window_title} ({self.sys_file}{" *" if self.unsaved else ""})')

    def show_dialog(self, dialog: Type[NodeDialog], node: GeoNode):
        form = dialog(node, self.sys)
        code = form.exec_()
        if code:
            self.unsaved = True
            self.render_ui()


def main():
    app = QtWidgets.QApplication([])
    application = MainWin()
    application.show()

    app.setStyleSheet(st.stylesheet)
    application.setStyleSheet(st.stylesheet)

    sys.exit(app.exec())


if __name__ == '__main__':
    r = RouteBuilder(init_system())
    routes = r.calc_routes()
    main()
