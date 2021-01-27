from PyQt5 import QtCore, QtGui, QtWidgets
import pyodbc
from PyQt5.QtWidgets import QWidget, QApplication, QSystemTrayIcon, QStyle, QAction, qApp, QMenu, QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox
from authorizationui import Ui_Dialog
from PyQt5.QtCore import QRect
from admin.main import window as windowadmin
from editor.main import window as windoweditor
from common.main import window as windowcommon
from register import Dialog
class LoginDatabase():
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',
        SERVER='DESKTOP-775NG2O\MSSQLSERVER01',
        DATABASE=dbname,
        trusted_connection='yes')#Подключение к БД

    def is_table(self, table_name):
        query = "SELECT name from {table_name}".format(table_name=table_name)
        cursor = self.conn.execute(query)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True


class MainDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(MainDialog, self).__init__()
        self.ui=Ui_Dialog()
        self.ui.setupUi(self)

        self.loginDatabase = LoginDatabase('anime')
        if self.loginDatabase.is_table('Users'):
            pass
        else:
            self.loginDatabase.conn.execute("CREATE TABLE USERS(USERNAME TEXT NOT NULL, EMAIL TEXT, PASSWORD TEXT)")
            self.loginDatabase.conn.execute("INSERT INTO USERS VALUES(?, ?, ?)", 
                                           ('admin', 'admin@gmail.com', 'admin') 
            )
            self.loginDatabase.conn.commit()

        self.ui.login_btn.clicked.connect(self.loginCheck)
        self.ui.signup_btn.clicked.connect(self.signUpCheck)        

    def showMessageBox(self, title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def welcomeWindowShow(self):
        data=self.loginDatabase.conn.execute("select rights from users where name = (?)",(self.ui.uname_lineEdit.text())).fetchall()
        data=[elem[0] for elem in data]
        print(data)
        if(int(data[0])==2):
            self.ui.welcomeWindow = windowadmin(self.ui.uname_lineEdit.text())
            self.ui.welcomeWindow.show()
        if(int(data[0])==1):
            self.ui.welcomeWindow = windoweditor(self.ui.uname_lineEdit.text())
            self.ui.welcomeWindow.show()
        if(int(data[0])==0):
            self.ui.welcomeWindow = windowcommon(self.ui.uname_lineEdit.text())
            self.ui.welcomeWindow.show()

    def signUpShow(self):
        self.signUpWindow = Dialog(self)
        self.signUpWindow.show()

    def loginCheck(self):
        username = self.ui.uname_lineEdit.text()
        password = self.ui.pass_lineEdit.text()
        if (not username) or (not password):
            msg = QMessageBox.information(self, 'Внимание!', 'Вы не заполнили все поля.')
            return

        result = self.loginDatabase.conn.execute("SELECT * FROM Users WHERE name = ? AND password = ?",(username, password))
        if len(result.fetchall()):     
            self.welcomeWindowShow()
            self.hide()
            self.loginDatabase.conn.close()
        else:
            self.showMessageBox('Внимание!', 'Неправильное имя пользователя или пароль.')

    def signUpCheck(self):
        self.signUpShow()


if __name__ == "__main__":
    import sys
    app    = QtWidgets.QApplication(sys.argv)
    w = MainDialog()
    w.show()
    sys.exit(app.exec_())