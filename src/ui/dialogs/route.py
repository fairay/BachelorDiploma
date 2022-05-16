from copy import copy

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QLineEdit, QPushButton, \
    QListWidgetItem, QListWidget, QMessageBox, QLabel

from entities import *
from ui.fields import *
from ui.fields.delivery import DeliveryField
from ui.node_list import ParkingField


class RouteDialog(QDialog):
    window_title = 'Маршрут перевозки'
    route: Route
    sys: TransportSystem

    def __init__(self, route: Route, sys: TransportSystem):
        super().__init__()
        self.route = route
        self.sys = sys
        self.init_UI()
        self.init_data()

    def init_UI(self):
        self.setMinimumSize(800, 800)
        self.setWindowTitle(self.window_title)
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        cnt = QHBoxLayout(self)
        self.setLayout(cnt)

        self.content = QVBoxLayout()
        content = self.content
        content.setAlignment(Qt.AlignTop)
        content.setContentsMargins(3, 3, 3, 5)
        content.setSpacing(10)

        cnt.addItem(QSpacerItem(40, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))
        cnt.addItem(content)
        cnt.addItem(QSpacerItem(40, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.track_UI()
        self.nodes_UI()

    def track_UI(self):
        self.trackW = QLabel(self.route.track.name, self)
        self.content.addWidget(self.trackW)

    def nodes_UI(self):
        layout = QVBoxLayout()

        self.nodeListW = QListWidget(self)
        layout.addWidget(self.nodeListW)

        self.content.addItem(layout)
        return layout

    def init_data(self):
        for node, load in zip(self.route.nodes, self.route.loads):
            self.add_node(node, load)

    def add_node(self, node: GeoNode, load: ProductList):
        widget = DeliveryField(node, load)

        item = QListWidgetItem(self.nodeListW)
        item.setSizeHint(widget.sizeHint())
        self.nodeListW.addItem(item)
        self.nodeListW.setItemWidget(item, widget)
