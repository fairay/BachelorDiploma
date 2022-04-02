from copy import copy, deepcopy

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QLineEdit, QPushButton, \
    QWidget, QListWidgetItem, QListWidget, QComboBox, QDoubleSpinBox

from entities.geonode import *
from entities.system import TransportSystem


class LinkField(QWidget):
    def __init__(self, parent, node: GeoNode, options: List[GeoNode]):
        super(LinkField, self).__init__(parent=parent)

        self.node = node
        self.options = options
        self.initUI()
        self.initBinds()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.nodeW = QComboBox()
        for other in self.options:
            self.nodeW.addItem(other.name)

        self.nodeW.setCurrentIndex(self.options.index(self.node))
        # print("this", self.nodeW.model().item(1).setEnabled(False))
        # print("this", self.nodeW.model().item(1).setBackground(QBrush(QColor(150, 150, 150))))

        self.nodeW.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.layout.addWidget(self.nodeW)

        self.space = QSpacerItem(30, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)
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

    def initBinds(self):
        self.nodeW.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, index: int):
        pass

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.node_widget.setText(text)

    def clickEvent(self):
        pass

    def closeEvent(self, event):
        pass


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

        self.content = QVBoxLayout()
        content = self.content
        content.setAlignment(Qt.AlignTop)
        content.setContentsMargins(3, 3, 3, 5)
        content.setSpacing(10)

        cnt.addItem(QSpacerItem(40, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))
        cnt.addItem(content)
        cnt.addItem(QSpacerItem(40, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))

        #
        self.nameW = QLineEdit(self.node.name, self)
        content.addWidget(self.nameW)

        self.links_UI()
        self.additional_UI()
        self.buttons_UI()

        self._init_links()

    def links_UI(self):
        layout = QVBoxLayout()

        self.link_list = QListWidget(self)
        layout.addWidget(self.link_list)

        apply_btn = QPushButton("Добавить связь", self)
        layout.addWidget(apply_btn)

        self.content.addItem(layout)
        return layout

    def buttons_UI(self):
        layout = QVBoxLayout()

        applyW = QPushButton("Применить", self)
        applyW.clicked.connect(self.apply)
        layout.addWidget(applyW)

        layout.addWidget(QPushButton("Удалить", self))

        self.content.addItem(layout)

    def additional_UI(self):
        pass

    def update_node(self):
        self.node.name = self.nameW.text()

    def apply(self):
        self.update_node()
        self.source_node.update(self.node)
        self.close()
        print('Applied')

    def add_link(self, other: GeoNode):
        node_list = self.sys.node_arr
        node_list.remove(self.source_node)
        widget = LinkField(self, other, node_list)

        item = QListWidgetItem(self.link_list)
        item.setSizeHint(widget.sizeHint())
        self.link_list.addItem(item)
        self.link_list.setItemWidget(item, widget)

    def _init_links(self):
        for other in self.node.linked.keys():
            self.add_link(other)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pass
        # self.node = self.source_node

class WarehouseDialog(NodeDialog):
    def __init__(self, node: Warehouse, sys: TransportSystem):
        super(WarehouseDialog, self).__init__(node, sys)

    def additional_UI(self):
        apply_btn = QPushButton("Something for Warehouse", self)
        self.content.addWidget(apply_btn)
