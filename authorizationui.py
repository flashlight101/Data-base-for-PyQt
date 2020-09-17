from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QSystemTrayIcon, QStyle, QAction, qApp, QMenu, QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.Qt import *
import PyQt5
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(496, 265)
        self.u_name_label = QLabel(Dialog)
        self.u_name_label.setGeometry(QRect(150, 105, 91, 30))
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.u_name_label.setFont(font)
        self.u_name_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.u_name_label.setObjectName("u_name_label")
        self.pass_label = QLabel(Dialog)
        self.pass_label.setGeometry(QRect(140, 150, 91, 21))
        font = QFont()
        font.setPointSize(10)
        self.pass_label.setFont(font)
        self.pass_label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.pass_label.setObjectName("pass_label")
        self.uname_lineEdit = QLineEdit(Dialog)
        self.uname_lineEdit.setGeometry(QRect(230, 110, 113, 25))
        self.uname_lineEdit.setObjectName("uname_lineEdit")
        self.pass_lineEdit = QLineEdit(Dialog)
        self.pass_lineEdit.setGeometry(QRect(230, 150, 113, 25))
        self.pass_lineEdit.setObjectName("pass_lineEdit")
        self.login_btn = QPushButton(Dialog)
        self.login_btn.setGeometry(QRect(210, 200, 70, 30))
        self.login_btn.setObjectName("login_btn")
        self.signup_btn = QPushButton(Dialog)
        self.signup_btn.setGeometry(QRect(290, 200, 70, 30))
        self.signup_btn.setObjectName("signup_btn")
        self.label = QLabel(Dialog)
        self.label.setGeometry(QRect(190, 10, 211, 51))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Авторизация"))
        self.u_name_label.setText(_translate("Dialog", "Login"))
        self.pass_label.setText(_translate("Dialog", "Password"))
        self.login_btn.setText(_translate("Dialog", "Login"))
        self.signup_btn.setText(_translate("Dialog", "Sign Up"))
        self.label.setText(_translate("Dialog", "Авторизация"))