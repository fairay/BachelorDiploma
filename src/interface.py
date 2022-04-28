from PyQt5.QtCore import Qt

from ui.gui import *


class GuiMainWin(Ui_MainWindow):
    scene_bg_color = Qt.black
    gen = []
    proc = []

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.set_binds()

    def set_binds(self):
        pass

    def err_msg(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(
            "<html><head/><body><p><span style=\" font-size:14pt;\">"
            "{:}"
            " </span></p></body></html>".format(text))
        msg.setWindowTitle("Ошибка")
        msg.exec_()
