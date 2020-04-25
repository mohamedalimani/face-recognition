# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reconGUI2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addnewface(object):
    def setupUi(self, addnewface):
        addnewface.setObjectName("addnewface")
        addnewface.resize(800, 544)
        self.centralwidget = QtWidgets.QWidget(addnewface)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(170, 10, 431, 361))
        self.graphicsView.setObjectName("graphicsView")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(260, 430, 241, 51))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 380, 531, 41))
        font = QtGui.QFont()
        font.setFamily("URW Bookman L")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        addnewface.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(addnewface)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menunavigate = QtWidgets.QMenu(self.menubar)
        self.menunavigate.setObjectName("menunavigate")
        addnewface.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(addnewface)
        self.statusbar.setObjectName("statusbar")
        addnewface.setStatusBar(self.statusbar)
        self.actionvers_reconnaissance_facial = QtWidgets.QAction(addnewface)
        self.actionvers_reconnaissance_facial.setObjectName("actionvers_reconnaissance_facial")
        self.menunavigate.addAction(self.actionvers_reconnaissance_facial)
        self.menubar.addAction(self.menunavigate.menuAction())

        self.retranslateUi(addnewface)
        QtCore.QMetaObject.connectSlotsByName(addnewface)

    def retranslateUi(self, addnewface):
        _translate = QtCore.QCoreApplication.translate
        addnewface.setWindowTitle(_translate("addnewface", "MainWindow"))
        self.label.setText(_translate("addnewface", "tapez le nom du personnage que tu veux ajouter"))
        self.menunavigate.setTitle(_translate("addnewface", "navigate"))
        self.actionvers_reconnaissance_facial.setText(_translate("addnewface", "vers reconnaissance facial"))
        self.actionvers_reconnaissance_facial.setStatusTip(_translate("addnewface", "ouvrir la page de réconnaissance faciale"))

