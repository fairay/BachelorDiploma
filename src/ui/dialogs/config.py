from typing import Optional

from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QPushButton, \
    QMessageBox, QLabel, QSlider, QCheckBox, QTimeEdit, QDoubleSpinBox

from entities import Route, GeoNode
from entities.route_builder import MAX_ITER

import datetime as dt

class GUIConfig(object):
    def __init__(self):
        self.iters = MAX_ITER
        self.show_labels = True

        self.cur_node: Optional[GeoNode] = None
        self.cur_route: Optional[Route] = None

        self.begin_t = dt.timedelta(hours=9)
        self.end_t = dt.timedelta(hours=18)

        self.prod_volume = 0.1


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
        self.schedule_UI()
        self.prod_volume_UI()

        self.content.addItem(QSpacerItem(40, 10, QSizePolicy.Fixed, QSizePolicy.Minimum))
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

    def schedule_UI(self):
        layout = QHBoxLayout()

        layout.addWidget(QLabel('Рабочий день', self))

        t_str = str(self.config.begin_t)
        t_new = QTime.fromString(t_str, "h:mm:ss")
        self.begin_timeW = QTimeEdit(t_new, self)
        layout.addWidget(self.begin_timeW)

        t_str = str(self.config.end_t)
        t_new = QTime.fromString(t_str, "h:mm:ss")
        self.end_timeW = QTimeEdit(t_new, self)
        layout.addWidget(self.end_timeW)

        self.content.addItem(layout)

    def prod_volume_UI(self):
        layout = QHBoxLayout()

        layout.addWidget(QLabel('Объём тары', self))

        self.prod_volumeW = QDoubleSpinBox(self)
        self.prod_volumeW.setValue(self.config.prod_volume)
        self.prod_volumeW.setSingleStep(0.01)
        layout.addWidget(self.prod_volumeW)

        layout.addWidget(QLabel('м³', self))
        self.content.addItem(layout)

    def buttons_UI(self):
        layout = QHBoxLayout()

        applyW = QPushButton("Применить", self)
        applyW.clicked.connect(self.apply)
        layout.addWidget(applyW)

        self.content.addItem(layout)

    def update_config(self):
        self.config.iters = self.iterW.value()
        self.config.show_labels = self.show_labelsW.isChecked()

        t = self.begin_timeW.time().toPyTime()
        self.config.begin_t = dt.timedelta(hours=t.hour, minutes=t.minute)

        t = self.end_timeW.time().toPyTime()
        self.config.end_t = dt.timedelta(hours=t.hour, minutes=t.minute)

        self.config.prod_volume = self.prod_volumeW.value()

    def apply(self):
        try:
            self.update_config()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', str(e))
            return

        self.accept()
        self.close()
