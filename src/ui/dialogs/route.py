import datetime as dt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QListWidgetItem, QListWidget, \
    QLabel

from entities import *
from entities.route_shedule import RouteSchedule
from ui.fields.delivery import DeliveryField


class RouteDialog(QDialog):
    window_title = 'Маршрут перевозки'
    route: RouteSchedule
    sys: TransportSystem

    def __init__(self, route: RouteSchedule, truck_i: int, sys: TransportSystem):
        super().__init__()
        self.route = route
        self.sys = sys
        self.truck_i = truck_i

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
        self.trackW = QLabel(f'[{self.truck_i}] {self.route.track.name}', self)
        self.content.addWidget(self.trackW)

    def nodes_UI(self):
        layout = QVBoxLayout()

        self.nodeListW = QListWidget(self)
        layout.addWidget(self.nodeListW)

        self.content.addItem(layout)
        return layout

    def init_data(self):
        for node, load, arrival, departure in self.route.nodes_schedule:
            self.add_node(node, load, arrival, departure)

    def add_node(self, node: GeoNode, load: ProductList, arrival: dt.timedelta, departure: dt.timedelta):
        widget = DeliveryField(node, load, arrival, departure)

        item = QListWidgetItem(self.nodeListW)
        item.setSizeHint(widget.sizeHint())
        self.nodeListW.addItem(item)
        self.nodeListW.setItemWidget(item, widget)
