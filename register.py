from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QSystemTrayIcon, QStyle, QAction, qApp, QMenu, QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from registerui import Ui_signUp
class Dialog(QDialog, Ui_signUp):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.signup_btn.clicked.connect(self.insertData)

    @pyqtSlot()
    def insertData(self):
        username = self.uname_lineEdit.text()
        email    = self.email_lineEdit.text()
        password = self.password_lineEdit.text()

        if (not username) or (not email) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        result = self.parent.loginDatabase.conn.execute("SELECT * FROM USERS WHERE NAME = ?", (username,))
        if result.fetchall():
            msg = QMessageBox.information(self, 'Внимание!', 'Пользоватеть с таким именем уже зарегистрирован.')
        else:
            self.parent.loginDatabase.conn.execute("INSERT INTO USERS VALUES(?, ?, ?,0)", 
                                                   (username, email, password))
            self.parent.loginDatabase.conn.commit()
            self.close()


if __name__ == "__main__":
    import sys
    app    = QApplication(sys.argv)
    w = Dialog()
    w.show()
    sys.exit(app.exec_())