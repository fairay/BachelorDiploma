from typing import Callable, Any, Type

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy

from entities import GeoNode
from entities.nodes import Warehouse, Parking, Consumer
from ui.dialogs.consumer import ConsumerDialog
from ui.dialogs.node import NodeDialog
from ui.dialogs.parking import ParkingDialog
from ui.dialogs.warehouse import WarehouseDialog


class ListField(QWidget):
    dialog: Type[NodeDialog]

    def __init__(self, node: GeoNode, show_dialog: Callable[[Type[NodeDialog], GeoNode], Any]):
        super(ListField, self).__init__(parent=None)
        self.node = node
        self.show_dialog = show_dialog

        self.setProperty('class', 'list')
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.titleW = QLabel(node.name)
        self.layout.addWidget(self.titleW)

        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        # self.titleW.setStyleSheet(''' color: rgb(255, 0, 0); ''')

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.clickEvent()
        self.updateContent()

    def updateContent(self) -> None:
        self.titleW.setText(self.node.name)

    def clickEvent(self):
        try:
            self.show_dialog(self.dialog, self.node)
        except Exception as e:
            print(e)


class ParkingField(ListField):
    dialog = ParkingDialog

    def __init__(self, node: Parking, show_dialog: Callable[[Type[NodeDialog], GeoNode], Any]):
        super(ParkingField, self).__init__(node, show_dialog)
        self.titleW.setProperty('class', 'pTitle')


class WarehouseField(ListField):
    dialog = WarehouseDialog

    def __init__(self, node: Warehouse, show_dialog: Callable[[Type[NodeDialog], GeoNode], Any]):
        super(WarehouseField, self).__init__(node, show_dialog)
        self.titleW.setProperty('class', 'wTitle')


class ConsumerField(ListField):
    dialog = ConsumerDialog

    def __init__(self, node: Consumer, show_dialog: Callable[[Type[NodeDialog], GeoNode], Any]):
        super(ConsumerField, self).__init__(node, show_dialog)
        self.titleW.setProperty('class', 'cTitle')
