# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diploma.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1075, 800)
        MainWindow.setMinimumSize(QtCore.QSize(1075, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1075, 800))
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 10, 531, 721))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.GraphWidget = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.GraphWidget.setContentsMargins(0, 0, 0, 0)
        self.GraphWidget.setObjectName("GraphWidget")
        self.NodeList = QtWidgets.QListWidget(self.centralwidget)
        self.NodeList.setGeometry(QtCore.QRect(560, 10, 501, 351))
        self.NodeList.setObjectName("NodeList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1075, 30))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menu_4)
        self.menu_5.setObjectName("menu_5")
        self.menu_6 = QtWidgets.QMenu(self.menu_4)
        self.menu_6.setObjectName("menu_6")
        self.menu_7 = QtWidgets.QMenu(self.menubar)
        self.menu_7.setObjectName("menu_7")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.action_6 = QtWidgets.QAction(MainWindow)
        self.action_6.setObjectName("action_6")
        self.action_8 = QtWidgets.QAction(MainWindow)
        self.action_8.setObjectName("action_8")
        self.action_9 = QtWidgets.QAction(MainWindow)
        self.action_9.setObjectName("action_9")
        self.action_10 = QtWidgets.QAction(MainWindow)
        self.action_10.setObjectName("action_10")
        self.action_11 = QtWidgets.QAction(MainWindow)
        self.action_11.setObjectName("action_11")
        self.menu.addAction(self.action)
        self.menu_5.addAction(self.action_4)
        self.menu_5.addAction(self.action_5)
        self.menu_5.addAction(self.action_6)
        self.menu_6.addAction(self.action_8)
        self.menu_6.addAction(self.action_9)
        self.menu_6.addAction(self.action_10)
        self.menu_4.addAction(self.menu_5.menuAction())
        self.menu_4.addSeparator()
        self.menu_4.addAction(self.menu_6.menuAction())
        self.menu_7.addAction(self.action_11)
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_7.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Оптимизация маршрутов поставок"))
        self.menu.setTitle(_translate("MainWindow", "Склады"))
        self.menu_2.setTitle(_translate("MainWindow", "Потребители"))
        self.menu_3.setTitle(_translate("MainWindow", "Заказы"))
        self.menu_4.setTitle(_translate("MainWindow", "Файл"))
        self.menu_5.setTitle(_translate("MainWindow", "Экспорт"))
        self.menu_6.setTitle(_translate("MainWindow", "Импорт"))
        self.menu_7.setTitle(_translate("MainWindow", "Транспорт"))
        self.action.setText(_translate("MainWindow", "Добавить"))
        self.action_4.setText(_translate("MainWindow", "Карта"))
        self.action_5.setText(_translate("MainWindow", "Запасы"))
        self.action_6.setText(_translate("MainWindow", "Заказы"))
        self.action_8.setText(_translate("MainWindow", "Карта"))
        self.action_9.setText(_translate("MainWindow", "Запасы"))
        self.action_10.setText(_translate("MainWindow", "Заказы"))
        self.action_11.setText(_translate("MainWindow", "Добавить"))
