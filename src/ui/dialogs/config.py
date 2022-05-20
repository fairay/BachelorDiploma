from entities.route_builder import MAX_ITER
from copy import copy

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QLineEdit, QPushButton, \
    QListWidgetItem, QListWidget, QMessageBox, QLabel, QSlider

from entities import *
from ui.fields import *


class GUIConfig(object):
    def __init__(self):
        self.iters = MAX_ITER


class ConfigDialog(QDialog):
    window_title = 'Настройки системы'

    def __init__(self, config: GUIConfig):
        super(ConfigDialog, self).__init__()
        self.config = config

        self.init_UI()

    def init_UI(self):
        self.setMinimumSize(800, 800)
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
        self.main_UI()
        self.buttons_UI()

    def title_UI(self):
        self.titleW = QLabel('Настройки системы', self)
        self.content.addWidget(self.titleW)

    def _upd_iter(self):
        self.iterLabel.setText(f'Максимальное количество итераций: {self.iterW.value()}')

    def main_UI(self):
        print('hello')
        layout = QVBoxLayout()

        self.iterLabel = QLabel('Максимальное количество итераций', self)
        layout.addWidget(self.iterLabel)

        self.iterW = QSlider(Qt.Horizontal, self)
        self.iterW.setRange(0, MAX_ITER)
        self.iterW.setPageStep(10)
        self.iterW.setValue(self.config.iters)
        self.iterW.valueChanged.connect(self._upd_iter)
        self._upd_iter()
        layout.addWidget(self.iterW)

        self.content.addItem(layout)
        self.content.addItem(QSpacerItem(40, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))

    def buttons_UI(self):
        layout = QHBoxLayout()

        applyW = QPushButton("Применить", self)
        applyW.clicked.connect(self.apply)
        layout.addWidget(applyW)

        self.content.addItem(layout)

    def update_config(self):
        self.config.iters = self.iterW.value()

    def apply(self):
        try:
            self.update_config()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
            return

        self.setResult(1)
        self.close()
