from copy import copy, deepcopy

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QLineEdit, QPushButton, \
    QWidget, QListWidgetItem, QListWidget, QComboBox, QDoubleSpinBox, QErrorMessage, QMessageBox

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

        dist = self.parent().node.dist(self.node) if self.parent().node.is_linked(self.node) else 1.0
        self.distW = QDoubleSpinBox()
        self.distW.setValue(dist)
        self.distW.setFrame(0)
        self.layout.addWidget(self.distW)

        time = self.parent().node.time(self.node) if self.parent().node.is_linked(self.node) else 1.0
        self.timeW = QDoubleSpinBox()
        self.timeW.setValue(time)
        self.timeW.setFrame(0)
        self.layout.addWidget(self.timeW)

        self.editButton = QPushButton("🗑️")
        self.editButton.setMaximumWidth(30)
        self.editButton.clicked.connect(self.clickEvent)
        self.layout.addWidget(self.editButton)

        # setStyleSheet
        self.nodeW.setStyleSheet('color: rgb(255, 0, 0);')

    def initBinds(self):
        self.nodeW.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, index: int):
        self.node = self.options[index]

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.node_widget.setText(text)

    def clickEvent(self):
        self.parent().parent().parent().delete_link(self)

    def closeEvent(self, event):
        pass

    @property
    def dist(self) -> float: return self.distW.value()
    @dist.setter
    def dist(self, value: float): self.distW.setValue(value)

    @property
    def time(self) -> float: return self.timeW.value()
    @time.setter
    def time(self, value: float): self.timeW.setValue(value)


class NodeDialog(QDialog):
    def __init__(self, node: GeoNode, sys: TransportSystem):
        super().__init__()
        self.node = copy(node)
        self.source_node = node
        self.sys = sys
        self.init_UI()
        self.init_links()

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

        self.title_UI()
        self.links_UI()
        self.additional_UI()
        self.buttons_UI()

    def title_UI(self):
        self.titleW = QLineEdit(self.node.name, self)
        self.content.addWidget(self.titleW)

    def links_UI(self):
        layout = QVBoxLayout()

        self.linkW = QListWidget(self)
        layout.addWidget(self.linkW)

        self.add_linkW = QPushButton("Добавить связь", self)
        self.add_linkW.clicked.connect(self.add_new_link)
        layout.addWidget(self.add_linkW)

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
        name = self.titleW.text()
        if name == "":
            raise Exception("Имя не задано")

        nodes = list(filter(lambda n: n.name == name, self.sys.node_arr))
        if len(nodes) > 0 and nodes != [self.source_node]:
            raise Exception("Имя пункта уже занято")

        self.node.name = name

        new_dict = {}
        for i in range(self.linkW.count()):
            item = self.linkW.item(i)
            widget = self.linkW.itemWidget(item)

            if widget.node in new_dict:
                raise Exception("Несколько связей с %s" % str(widget.node))

            new_dict[widget.node] = {'dist': widget.dist, 'time': widget.time}

        self.node.unlink()
        for k, v in new_dict.items():
            self.node.add_node(k, **v, symmetric=False)

    def apply(self):
        try:
            self.update_node()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
            return

        self.source_node.update(self.node)
        self.close()
        print('Applied')

    def add_new_link(self):
        node_list = self.sys.node_arr
        node_list.remove(self.source_node)

        for i in range(self.linkW.count()):
            item = self.linkW.item(i)
            widget = self.linkW.itemWidget(item)
            if widget.node in node_list:
                node_list.remove(widget.node)

        if len(node_list):
            self.add_link(node_list[0])

    def add_link(self, other: GeoNode):
        node_list = self.sys.node_arr
        node_list.remove(self.source_node)
        widget = LinkField(self, other, node_list)

        item = QListWidgetItem(self.linkW)
        item.setSizeHint(widget.sizeHint())
        self.linkW.addItem(item)
        self.linkW.setItemWidget(item, widget)

    def init_links(self):
        for other in self.node.linked.keys():
            self.add_link(other)

    def delete_link(self, link: LinkField):
        for i in range(self.linkW.count()):
            item = self.linkW.item(i)
            widget = self.linkW.itemWidget(item)
            if widget == link:
                self.linkW.takeItem(i)
                return

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pass
        # self.node = self.source_node


class WarehouseDialog(NodeDialog):
    def __init__(self, node: Warehouse, sys: TransportSystem):
        super(WarehouseDialog, self).__init__(node, sys)

    def additional_UI(self):
        apply_btn = QPushButton("Something for Warehouse", self)
        self.content.addWidget(apply_btn)
