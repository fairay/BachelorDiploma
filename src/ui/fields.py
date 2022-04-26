from typing import List

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QSizePolicy, QSpacerItem, QDoubleSpinBox, QPushButton

from entities.geonode import GeoNode


class LinkField(QWidget):
    def __init__(self, parent, node: GeoNode, options: List[GeoNode]):
        super(LinkField, self).__init__(parent=parent)

        self.dialog = parent
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
        self.dialog.delete_link(self)

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