
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Users(object):
    def setupUi(self, Form):
        Form.setObjectName("UsersWin")
        Form.resize(640, 480)
        self.tableUsers=QtWidgets.QTableWidget(Form)
        self.tableUsers.setGeometry(QtCore.QRect(0, 0, 640, 300))
        self.labeldelete=QtWidgets.QLabel(Form)
        self.labeldelete.setGeometry(QtCore.QRect(20,350,450,40))
        self.labeldelete.setText("Введите id пользователя, которого хотите удалить")
        self.deleteusers=QtWidgets.QLineEdit(Form)
        self.deleteusers.setGeometry(QtCore.QRect(10, 390, 50, 30))
        self.deletebutton=QtWidgets.QPushButton(Form)
        self.deletebutton.setGeometry(QtCore.QRect(80,390,60,30))
        self.deletebutton.setText("Удалить")
        QtCore.QMetaObject.connectSlotsByName(Form)


