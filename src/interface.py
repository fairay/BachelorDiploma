from typing import List, Type

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QFileDialog, QListWidgetItem
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from entities import TransportSystem, Route, Parking, Warehouse, Consumer, GeoNode, RouteBuilder
from graphics import get_figure
from ui.dialogs import ParkingDialog, WarehouseDialog, ConsumerDialog, NodeDialog
from ui.dialogs.config import GUIConfig, ConfigDialog
from ui.dialogs.route import RouteDialog
from ui.fields.route import RouteField
from ui.gui import *
from ui.node_list import ListField, ParkingField, WarehouseField, ConsumerField


class GuiMainWin(Ui_MainWindow):
    scene_bg_color = Qt.black
    gen = []
    proc = []

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.set_binds()

    def set_binds(self):
        pass

    def err_msg(self, text: str):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(
            "<html><head/><body><p><span style=\" font-size:14pt;\">"
            f"{text}"
            " </span></p></body></html>")
        msg.setWindowTitle("Ошибка")
        msg.exec_()


class MainWin(QtWidgets.QMainWindow):
    ui: GuiMainWin = None
    window_title = 'Оптимизация маршрутов поставок'

    sys: TransportSystem
    routes: List[Route]

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
        self.routes = []
        self.config = GUIConfig()

        self.render_ui()
        self.set_binds()

    def set_binds(self):
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.export_click)
        self.ui.routeList.clicked.connect(self.build_figure)
        self.ui.nodeList.clicked.connect(self.build_figure)

        self.ui.import_action.triggered.connect(self.import_action)
        self.ui.export_action.triggered.connect(self.export_action)

        self.ui.action_parking.triggered.connect(self.action_parking)
        self.ui.action_warehouse.triggered.connect(self.action_warehouse)
        self.ui.action_consumer.triggered.connect(self.action_consumer)

        self.ui.action_config.triggered.connect(self.config_dialog)

        self.ui.calcRoutesW.clicked.connect(self.build_routes)

    def action_parking(self):
        if self.sys.parking:
            self.ui.err_msg("Стоянка уже существует")
            return

        node = Parking()
        self.sys.add_parking(node)
        self.unsaved = True

        self.render_ui()
        self.node_dialog(ParkingDialog, node)

    def action_warehouse(self):
        node = Warehouse()
        self.sys.add_warehouse(node)
        self.unsaved = True

        self.render_ui()
        self.node_dialog(WarehouseDialog, node)

    def action_consumer(self):
        node = Consumer()
        self.sys.add_consumer(node)
        self.unsaved = True

        self.render_ui()
        self.node_dialog(ConsumerDialog, node)

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
        self.clean_list()
        self.clean_routes()
        self.sys = TransportSystem.Loader.load(file_name)
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
        TransportSystem.Loader.save(self.sys, file_name)
        self.unsaved = False
        self.sys_file = file_name

    def build_figure(self):
        cur_route_i = self.ui.routeList.currentRow()
        cur_route = self.routes[cur_route_i] if cur_route_i != -1 else None

        cur_node_i = self.ui.nodeList.currentRow()
        cur_node = self.sys.nodes[cur_node_i] if cur_node_i != -1 else None

        fig = get_figure(self.sys, cur_route, cur_node)

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
        self.ui.nodeList.clear()

    def show_node(self, widget: ListField):
        item = QListWidgetItem(self.ui.nodeList)
        item.setSizeHint(widget.sizeHint())
        self.ui.nodeList.addItem(item)
        self.ui.nodeList.setItemWidget(item, widget)

    def render_ui(self):
        self.clean_list()

        if self.sys.parking:
            self.show_node(ParkingField(self.sys.parking, self.node_dialog))
        for w_node in self.sys.warehouses:
            self.show_node(WarehouseField(w_node, self.node_dialog))
        for c_node in self.sys.consumers:
            self.show_node(ConsumerField(c_node, self.node_dialog))

        self.build_figure()

        self.setWindowTitle(f'{self.window_title} ({self.sys_file}{" *" if self.unsaved else ""})')

    def clean_routes(self):
        self.ui.routeList.clear()
        self.routes = []

    def show_route(self, r: Route):
        widget = RouteField(r, self.route_dialog)
        item = QListWidgetItem(self.ui.routeList)
        item.setSizeHint(widget.sizeHint())
        self.ui.routeList.addItem(item)
        self.ui.routeList.setItemWidget(item, widget)

    def build_routes(self):
        self.clean_routes()
        try:
            route_builder = RouteBuilder(self.sys)
            self.routes = route_builder.calc_routes(self.config.iters)
        except Exception as e:
            self.ui.err_msg(str(e))

        for r in self.routes:
            self.show_route(r)
        self.render_ui()

    def node_dialog(self, dialog: Type[NodeDialog], node: GeoNode):
        form = dialog(node, self.sys)
        code = form.exec_()
        if code:
            self.unsaved = True
            self.clean_routes()
            self.render_ui()

    def route_dialog(self, route: Route):
        form = RouteDialog(route, self.sys)
        _ = form.exec_()

    def config_dialog(self):
        form = ConfigDialog(self.config)
        code = form.exec_()

        if code:
            self.clean_routes()
            self.render_ui()
