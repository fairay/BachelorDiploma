from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy

from entities import Route


class RouteField(QWidget):
    route: Route

    def __init__(self, route: Route):
        super(RouteField, self).__init__(parent=None)
        self.route = route

        self.setProperty('class', 'list')
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.titleW = QLabel()
        self.layout.addWidget(self.titleW)

        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.updateContent()
        # self.titleW.setStyleSheet(''' color: rgb(255, 0, 0); ''')

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.clickEvent()
        self.updateContent()

    def updateContent(self) -> None:
        self.titleW.setText(str(self.route))

    def clickEvent(self):
        pass

    def closeEvent(self, event):
        print('onePopUp : close event')
