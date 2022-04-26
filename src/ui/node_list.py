from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy

from entities.geonode import GeoNode, Warehouse, Parking
from ui.node_dialog import NodeDialog, WarehouseDialog, ParkingDialog
from typing import Callable, Any, Type


class ListField(QWidget):
    def __init__(self, node: GeoNode, show_dialog: Callable[[Type[NodeDialog], GeoNode], Any]):
        super(ListField, self).__init__(parent=None)
        self.node = node
        self.show_dialog = show_dialog

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.titleW = QLabel(node.name)
        self.layout.addWidget(self.titleW)

        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.titleW.setStyleSheet(''' color: rgb(255, 0, 0); ''')

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.clickEvent()
        self.updateContent()

    def updateContent(self) -> None:
        self.titleW.setText(self.node.name)

    def clickEvent(self):
        pass

    def closeEvent(self, event):
        print('onePopUp : close event')


class ParkingField(ListField):
    def __init__(self, node: Parking, show_dialog: Callable[[Type[NodeDialog], GeoNode], Any]):
        super(ParkingField, self).__init__(node, show_dialog)
        self.titleW.setStyleSheet('color: rgb(200, 100, 0);')

    def clickEvent(self):
        try:
            self.show_dialog(ParkingDialog, self.node)
        except Exception as e:
            print(e)


class WarehouseField(ListField):
    def __init__(self, node: Warehouse, show_dialog: Callable[[Type[NodeDialog], GeoNode], Any]):
        super(WarehouseField, self).__init__(node, show_dialog)
        self.titleW.setStyleSheet('color: rgb(100, 150, 100);')

    def clickEvent(self):
        try:
            self.show_dialog(WarehouseDialog, self.node)
        except Exception as e:
            print(e)
