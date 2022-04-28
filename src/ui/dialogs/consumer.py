from PyQt5.QtWidgets import QPushButton

from entities import Warehouse, TransportSystem
from ui.dialogs.node import NodeDialog


class ConsumerDialog(NodeDialog):
    window_title = 'Параметры потребителя'

    def __init__(self, node: Warehouse, sys: TransportSystem):
        super(ConsumerDialog, self).__init__(node, sys)

    def additional_UI(self):
        apply_btn = QPushButton("Something for Consumer", self)
        self.content.addWidget(apply_btn)
