from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QDoubleSpinBox

from entities.transport import Transport


class TrackFiled(QWidget):
    def __init__(self, parent, track: Transport):
        super(TrackFiled, self).__init__(parent=parent)

        self.dialog = parent
        self.track = track
        self.initUI()
        self.initBinds()

    def initUI(self):
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.titleW = QLineEdit(self.track.name, self)
        self.layout.addWidget(self.titleW)

        volume = self.track.volume
        self.volumeW = QDoubleSpinBox()
        self.volumeW.setValue(volume)
        self.volumeW.setFrame(0)
        self.layout.addWidget(self.volumeW)

        cons = self.track.cons
        self.consW = QDoubleSpinBox()
        self.consW.setValue(cons)
        self.consW.setFrame(0)
        self.layout.addWidget(self.consW)

        self.editButton = QPushButton("🗑️")
        self.editButton.setMaximumWidth(30)
        self.layout.addWidget(self.editButton)

    def initBinds(self):
        self.editButton.clicked.connect(self.deleteEvent)

    def deleteEvent(self):
        self.dialog.delete_track(self)

    @property
    def title(self) -> str: return self.titleW.text()

    @title.setter
    def title(self, value: str): self.titleW.setText(value)

    @property
    def volume(self) -> float: return self.volumeW.value()

    @volume.setter
    def volume(self, value: float): self.volumeW.setValue(value)

    @property
    def cons(self) -> float: return self.consW.value()

    @cons.setter
    def cons(self, value: float): self.consW.setValue(value)

    @property
    def new_track(self) -> Transport:
        new_t = Transport(self.title)
        new_t.cons = self.cons
        new_t.volume = self.volume
        return new_t
