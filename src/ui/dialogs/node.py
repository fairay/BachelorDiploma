from copy import copy

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QLineEdit, QPushButton, \
    QListWidgetItem, QListWidget, QMessageBox

from entities import *
from ui.fields import *


class NodeDialog(QDialog):
    window_title = '...'

    def __init__(self, node: GeoNode, sys: TransportSystem):
        super().__init__()
        self.node = copy(node)
        self.source_node = node
        self.sys = sys
        self.init_UI()
        self.init_links()

    def init_UI(self):
        self.setMinimumSize(600, 300)
        self.setWindowTitle(self.window_title)
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
        layout = QHBoxLayout()

        applyW = QPushButton("Применить", self)
        applyW.clicked.connect(self.apply)
        layout.addWidget(applyW)

        layout.addItem(QSpacerItem(10, 0, QSizePolicy.Fixed, QSizePolicy.Fixed))

        deleteW = QPushButton("Удалить", self)
        deleteW.clicked.connect(self.delete)
        layout.addWidget(deleteW)

        self.content.addItem(layout)

    def additional_UI(self):
        pass

    def update_node(self):
        name = self.titleW.text()
        if name == "":
            raise Exception("Имя не задано")

        nodes = list(filter(lambda n: n.name == name, self.sys.nodes))
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
        self.setResult(1)
        self.close()
        print('Applied')

    def delete(self):
        del self.sys[self.source_node]

        self.setResult(1)
        self.close()
        print('Deleted')

    def add_new_link(self):
        node_list = self.sys.nodes
        node_list.remove(self.source_node)

        for i in range(self.linkW.count()):
            item = self.linkW.item(i)
            widget = self.linkW.itemWidget(item)
            if widget.node in node_list:
                node_list.remove(widget.node)

        if len(node_list):
            self.add_link(node_list[0])

    def add_link(self, other: GeoNode):
        node_list = self.sys.nodes
        node_list.remove(self.source_node)
        widget = LinkField(self, other, node_list)

        item = QListWidgetItem(self.linkW)
        item.setSizeHint(widget.sizeHint())
        self.linkW.addItem(item)
        self.linkW.setItemWidget(item, widget)

    def init_links(self):
        for other in self.node.linked.keys():
            self.add_link(other)

    def delete_link(self, del_link: LinkField):
        for i in range(self.linkW.count()):
            item = self.linkW.item(i)
            widget = self.linkW.itemWidget(item)
            if widget == del_link:
                self.linkW.takeItem(i)
                return

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        pass
        # self.node = self.source_node
