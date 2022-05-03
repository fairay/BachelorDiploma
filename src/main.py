import sys
from typing import Type, Optional

import PyQt5.QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QListWidgetItem, QFileDialog, QShortcut
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

import ui.styles as st
from entities import *
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

    c = Consumer([Product('кола', 15), Product('шоколад', 25)], "Потребитель №1")
    tsys.add_consumer(c)

    tsys.add_link(0, 1)
    tsys.add_link(0, 2)
    tsys.add_link(0, 3)
    tsys.add_link(1, 2)
    tsys.add_link(4, 3)

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
        self.canvas: Optional[FigureCanvasQTAgg] = None
        self.navbar: Optional[NavigationToolbar2QT] = None
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.export_click)

        self.sys_file = sys_file
        self.unsaved = False
        if tsys:
            self.sys = tsys
        else:
            self.import_sys(sys_file)

        self.setAnimated(True)
        self.setUpdatesEnabled(True)
        self.build_figure()
        self.render_ui()
        self.set_binds()

    def set_binds(self):
        self.ui.import_action.triggered.connect(self.import_action)
        self.ui.export_action.triggered.connect(self.export_action)

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

        if self.canvas:
            self.ui.GraphWidget.removeWidget(self.canvas)
        if self.navbar:
            self.ui.GraphWidget.removeWidget(self.navbar)

        self.canvas = FigureCanvasQTAgg(fig)
        self.navbar = NavigationToolbar2QT(self.canvas, self, coordinates=False)
        self.navbar.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Expanding, PyQt5.QtWidgets.QSizePolicy.Fixed)

        self.ui.GraphWidget.addWidget(self.canvas)
        self.ui.GraphWidget.addWidget(self.navbar)

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
    main()
