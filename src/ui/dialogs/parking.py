from copy import copy

from PyQt5.QtWidgets import QListWidgetItem, QVBoxLayout, QListWidget, QPushButton

from entities import *
from ui.dialogs.node import NodeDialog
from ui.fields import TrackFiled


class ParkingDialog(NodeDialog):
    window_title = 'Параметры стоянки'

    def __init__(self, node: Parking, sys: TransportSystem):
        super(ParkingDialog, self).__init__(node, sys)
        self.node: Parking = copy(node)
        self.source_node: Parking = node

    def delete_track(self, filed: TrackFiled):
        self.node.del_transport(filed.track)
        
        for i in range(self.trackW.count()):
            item = self.trackW.item(i)
            widget = self.trackW.itemWidget(item)
            if widget == filed:
                self.trackW.takeItem(i)
                return

    def add_track(self, track: Transport):
        widget = TrackFiled(self, track)

        item = QListWidgetItem(self.trackW)
        item.setSizeHint(widget.sizeHint())
        self.trackW.addItem(item)
        self.trackW.setItemWidget(item, widget)

    def add_new_track(self):
        self.add_track(Transport())

    def update_node(self):
        super(ParkingDialog, self).update_node()

        for i in range(self.trackW.count()):
            item = self.trackW.item(i)
            widget: TrackFiled = self.trackW.itemWidget(item)

            self.node.add_transport(widget.new_track)

    def track_UI(self):
        layout = QVBoxLayout()

        self.trackW = QListWidget(self)
        layout.addWidget(self.trackW)

        self.add_trackW = QPushButton("Добавить транспорт", self)
        self.add_trackW.clicked.connect(self.add_new_track)
        layout.addWidget(self.add_trackW)

        self.content.addItem(layout)
        return layout

    def fill_tracks(self):
        for track in self.node.transport:
            self.add_track(track)

    def additional_UI(self):
        self.track_UI()
        self.fill_tracks()
        # apply_btn = self.track_UI()
        # self.content.addWidget(apply_btn)
