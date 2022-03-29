from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton

from geonode import GeoNode, Warehouse
from ui.node_dialog import NodeDialog
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

        # self.editW = QPushButton("📝")
        # self.editW.setMaximumWidth(40)
        # self.editW.clicked.connect(self.clickEvent)
        # self.layout.addWidget(self.editW)

        # setStyleSheet
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


class WarehouseField(ListField):
    def __init__(self, node: Warehouse, show_dialog: Callable[[Type[NodeDialog], GeoNode], Any]):
        super(WarehouseField, self).__init__(node, show_dialog)

    def clickEvent(self):
        self.show_dialog(NodeDialog, self.node)
        #
        # form = NodeDialog(self.node)
        # form.exec_()

        print("Warehouse")
