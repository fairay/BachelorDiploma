import datetime as dt

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy, QVBoxLayout, QListWidget, QListWidgetItem, \
    QHBoxLayout

from entities import GeoNode, ProductList, Product
from entities.nodes import Warehouse
from ui.fields import ProductDeliveryField


class DeliveryField(QWidget):
    node: GeoNode
    load: ProductList
    arrival: dt.timedelta
    departure: dt.timedelta

    def __init__(self, node: GeoNode, load: ProductList, arrival: dt.timedelta, departure: dt.timedelta):
        super(DeliveryField, self).__init__(parent=None)
        self.node = node
        self.load = load
        self.arrival = arrival
        self.departure = departure

        self.init_ui()
        self.init_data()

    def init_ui(self):
        self.setProperty('class', 'list')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.label_ui()

        if not len(self.load):
            return

        self.loadW = QListWidget(self)
        self.loadW.setMinimumSize(0, 0)
        self.loadW.setProperty('class', 'delivery-list')
        self.loadW.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))
        self.layout.addWidget(self.loadW)

    def label_ui(self):
        layout = QHBoxLayout()

        self.titleW = QLabel(self.node.name, self)
        layout.addWidget(self.titleW)

        if self.arrival == self.departure:
            t = dt.datetime(2000, 1, 1) + self.arrival
            time_text = t.strftime("%H:%M")
        else:
            t1 = dt.datetime(2000, 1, 1) + self.arrival
            t2 = dt.datetime(2000, 1, 1) + self.departure
            time_text = f'{t1.strftime("%H:%M")} - {t2.strftime("%H:%M")}'

        timeW = QLabel(time_text, self)
        timeW.setAlignment(Qt.AlignRight)
        layout.addWidget(timeW)

        self.layout.addItem(layout)

    def init_data(self):
        for product in self.load:
            self.add_product(product)

    def add_product(self, product: Product):
        productW = ProductDeliveryField(self, product, picked=isinstance(self.node, Warehouse))
        item = QListWidgetItem(self.loadW)
        item.setSizeHint(productW.sizeHint())

        self.loadW.addItem(item)
        self.loadW.setItemWidget(item, productW)
        self.loadW.adjustSize()
        self.loadW.setMaximumSize(10000, item.sizeHint().height() * self.loadW.count() + 5)
