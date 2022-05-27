from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QPushButton, \
    QMessageBox, QLabel, QSlider, QCheckBox

from entities import Route, GeoNode
from entities.route_builder import MAX_ITER


class GUIConfig(object):
    def __init__(self):
        self.iters = MAX_ITER
        self.show_labels = True

        self.cur_node: Optional[GeoNode] = None
        self.cur_route: Optional[Route] = None


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
        self.max_iter_UI()
        self.show_labels_UI()
        self.buttons_UI()

    def title_UI(self):
        self.titleW = QLabel('Настройки системы', self)
        self.content.addWidget(self.titleW)

    def _upd_iter(self):
        self.iterLabel.setText(f'Максимальное количество итераций: {self.iterW.value()}')

    def max_iter_UI(self):
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

    def show_labels_UI(self):
        layout = QVBoxLayout()

        self.show_labelsW = QCheckBox('Отображать названия', self)
        self.show_labelsW.setChecked(self.config.show_labels)
        layout.addWidget(self.show_labelsW)

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
        self.config.show_labels = self.show_labelsW.isChecked()

    def apply(self):
        try:
            self.update_config()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
            return

        self.accept()
        self.close()
