from PyQt5.QtWidgets import QPushButton

from entities import Warehouse, TransportSystem
from ui.dialogs.node import NodeDialog


class WarehouseDialog(NodeDialog):
    window_title = 'Параметры склада'

    def __init__(self, node: Warehouse, sys: TransportSystem):
        super(WarehouseDialog, self).__init__(node, sys)

    def additional_UI(self):
        apply_btn = QPushButton("Something for Warehouse", self)
        self.content.addWidget(apply_btn)
