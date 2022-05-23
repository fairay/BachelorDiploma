from typing import Callable, Any

from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy

from entities.route_shedule import RouteSchedule
import datetime as dt

class RouteField(QWidget):
    route: RouteSchedule
    truck: int

    def __init__(self, route: RouteSchedule, truck: int, show_dialog: Callable[[RouteSchedule], Any]):
        super(RouteField, self).__init__(parent=None)
        self.route = route
        self.truck = truck
        self.show_dialog = show_dialog

        self.setProperty('class', 'list')
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.titleW = QLabel()
        self.layout.addWidget(self.titleW)

        self.layout.addItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.updateContent()

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.clickEvent()
        self.updateContent()

    def updateContent(self) -> None:
        t1 = dt.datetime(2000, 1, 1) + self.route.begin
        t2 = dt.datetime(2000, 1, 1) + self.route.end

        title = f'[{self.truck}] {t1.strftime("%H:%M")} - {t2.strftime("%H:%M")}'
        self.titleW.setText(title)

    def clickEvent(self):
        try:
            self.show_dialog(self.route)
        except Exception as e:
            print(e)
