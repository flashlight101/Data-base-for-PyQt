
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Log(object):
    def setupUi(self, Form):
        Form.setObjectName("LogWin")
        Form.resize(640, 520)
        self.tableUsers=QtWidgets.QTableWidget(Form)
        self.tableUsers.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.deletelog=QtWidgets.QPushButton(Form)
        self.deletelog.setGeometry(QtCore.QRect(320,490,100,30))
        self.deletelog.setText("Очистить логи")