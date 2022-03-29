from copy import copy

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QLineEdit, QPushButton, \
    QWidget, QListWidgetItem, QListWidget, QComboBox, QDoubleSpinBox

from geonode import *
from transport import TransportSystem


class LinkField(QWidget):
    def __init__(self, node: GeoNode):
        super(LinkField, self).__init__(parent=None)

        self.node = node

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.nodeW = QComboBox()
        self.nodeW.addItem(node.name)
        self.nodeW.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layout.addWidget(self.nodeW)

        self.space = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.space)

        self.distW = QDoubleSpinBox()
        self.distW.setValue(1.0)
        self.distW.setFrame(0)
        self.layout.addWidget(self.distW)

        self.timeW = QDoubleSpinBox()
        self.timeW.setValue(1.0)
        self.timeW.setFrame(0)
        self.layout.addWidget(self.timeW)

        self.editButton = QPushButton("🗑️")
        self.editButton.setMaximumWidth(30)
        self.editButton.clicked.connect(self.clickEvent)
        self.layout.addWidget(self.editButton)

        # setStyleSheet
        self.nodeW.setStyleSheet(''' color: rgb(255, 0, 0); ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.node_widget.setText(text)

    def clickEvent(self):
        pass

    def closeEvent(self, event):
        print('onePopUp : close event')


class NodeDialog(QDialog):
    def __init__(self, node: GeoNode, sys: TransportSystem):
        super().__init__()
        self.node = copy(node)
        self.source_node = node
        self.sys = sys
        self.init_UI()

    def init_UI(self):
        self.setMinimumSize(600, 300)
        self.setWindowTitle('Параметры склада')
        self.setWindowModality(Qt.ApplicationModal)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        cnt = QHBoxLayout(self)
        self.setLayout(cnt)

        content = QVBoxLayout()
        content.setAlignment(Qt.AlignTop)
        content.setContentsMargins(3, 3, 3, 5)

        cnt.addItem(QSpacerItem(100, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))
        cnt.addItem(content)
        cnt.addItem(QSpacerItem(100, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))

        #
        name_edit = QLineEdit(self.node.name, self)
        content.addWidget(name_edit)

        self.link_list = QListWidget(self)
        content.addWidget(self.link_list)

        apply_btn = QPushButton("Добавить связь", self)
        content.addWidget(apply_btn)
        self.space = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        content.addItem(self.space)

        apply_btn = QPushButton("Применить", self)
        content.addWidget(apply_btn)

        delete_btn = QPushButton("Удалить", self)
        content.addWidget(delete_btn)

        self._init_links()

    def add_link(self, other: GeoNode):
        try:
            widget = LinkField(other)

            item = QListWidgetItem(self.link_list)
            item.setSizeHint(widget.sizeHint())
            self.link_list.addItem(item)
            self.link_list.setItemWidget(item, widget)
        except Exception as e:
            print(e)

    def _init_links(self):
        for other in self.node.linked.keys():
            self.add_link(other)


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        print("canceled", self.node.name, "->", self.source_node.name)
        # self.node = self.source_node
