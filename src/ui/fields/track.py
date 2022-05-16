from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QDoubleSpinBox, QSpinBox

from entities import Transport


class TrackFiled(QWidget):
    track: Transport
    amount: int

    def __init__(self, parent, track: Transport, amount: int):
        super(TrackFiled, self).__init__(parent=parent)

        self.dialog = parent
        self.track = track
        self._amount = amount

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
        self.volumeW.setToolTip('Объём (м³)')
        self.layout.addWidget(self.volumeW)

        self.amountW = QSpinBox()
        self.amountW.setValue(self._amount)
        self.amountW.setMinimum(1)
        self.amountW.setFrame(0)
        self.amountW.setToolTip('Количество')
        self.layout.addWidget(self.amountW)

    def initBinds(self):
        pass

    @property
    def title(self) -> str: return self.titleW.text()

    @title.setter
    def title(self, value: str): self.titleW.setText(value)

    @property
    def volume(self) -> float: return self.volumeW.value()

    @volume.setter
    def volume(self, value: float): self.volumeW.setValue(value)

    @property
    def amount(self) -> int: return self.amountW.value()

    @amount.setter
    def amount(self, value: int): self.amountW.setValue(value)

    @property
    def new_track(self) -> Transport:
        new_t = Transport(self.title)
        new_t.volume = self.volume
        return new_t
