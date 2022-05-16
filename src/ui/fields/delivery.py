from PyQt5.QtWidgets import QWidget, QLabel, QSpacerItem, QSizePolicy, QVBoxLayout, QListWidget, QListWidgetItem

from entities import GeoNode, ProductList, Product
from entities.nodes import Warehouse
from ui.fields import ProductDeliveryField


class DeliveryField(QWidget):
    node: GeoNode
    load: ProductList

    def __init__(self, node: GeoNode, load: ProductList):
        super(DeliveryField, self).__init__(parent=None)
        self.node = node
        self.load = load

        self.init_ui()
        self.init_data()

    def init_ui(self):
        self.setProperty('class', 'list')
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.titleW = QLabel(self.node.name)
        self.layout.addWidget(self.titleW)

        if not len(self.load):
            return

        self.loadW = QListWidget(self)
        self.loadW.setMinimumSize(0, 0)
        self.loadW.setProperty('class', 'delivery-list')
        self.loadW.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding))
        self.layout.addWidget(self.loadW)

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
