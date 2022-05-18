from copy import copy

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QListWidget, QListWidgetItem

from entities import TransportSystem, Product
from entities.nodes import Consumer
from ui.dialogs.node import NodeDialog
from ui.fields import ProductFiled


class ConsumerDialog(NodeDialog):
    window_title = 'Параметры потребителя'

    def __init__(self, node: Consumer, sys: TransportSystem):
        super(ConsumerDialog, self).__init__(node, sys)
        self.node: Consumer = copy(node)
        self.source_node: Consumer = node

    def delete_product(self, filed: ProductFiled):
        self.node.del_product(filed.product)

        for i in range(self.productW.count()):
            item = self.productW.item(i)
            widget = self.productW.itemWidget(item)
            if widget == filed:
                self.productW.takeItem(i)
                return

    def add_product(self, product: Product):
        widget = ProductFiled(self, product)

        item = QListWidgetItem(self.productW)
        item.setSizeHint(widget.sizeHint())
        self.productW.addItem(item)
        self.productW.setItemWidget(item, widget)

    def add_new_product(self):
        self.add_product(Product("без имени", 1, self.sys.vol))

    def update_node(self):
        super(ConsumerDialog, self).update_node()

        for i in range(self.productW.count()):
            item = self.productW.item(i)
            widget: ProductFiled = self.productW.itemWidget(item)

            self.node.add_product(widget.new_product)

    def product_UI(self):
        layout = QVBoxLayout()

        self.productW = QListWidget(self)
        layout.addWidget(self.productW)

        self.add_productW = QPushButton("Добавить продукт", self)
        self.add_productW.clicked.connect(self.add_new_product)
        layout.addWidget(self.add_productW)

        self.content.addItem(layout)
        return layout

    def fill_products(self):
        for product in self.node.order:
            self.add_product(product)

    def additional_UI(self):
        self.product_UI()
        self.fill_products()
