from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from mainui import Ui_MainWindow
import sys
import pyodbc
class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window,self).__init__()
        self.data = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',SERVER='DESKTOP-775NG2O\MSSQLSERVER01',DATABASE='anime',trusted_connection='yes')
        self.flag=False
        self.init_UI()
    def init_UI(self,dynamic_row=2):
        self.cursor = self.data.cursor()
        self.column = self.cursor.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME='Customers'").fetchall()
        self.all_data=self.cursor.execute("select * from Customers").fetchall()
        self.column=[elem[0] for elem in self.column]
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        #self.dynamic_row=2#len(data)
        self.ui.pushButton.clicked.connect(self.all)
        self.ui.tableWidget.setColumnCount(len(self.column))
        self.ui.tableWidget.setRowCount(dynamic_row)
        self.ui.tableWidget.setHorizontalHeaderLabels(self.column)
        #self.ui.pushButton.clicked.connect(self.all)
        self.ui.tableWidget.setSortingEnabled(True)
        row = 0
        for tup in self.all_data:
            col = 0
 
            for item in tup:
                cellinfo = QTableWidgetItem(str(item))
                self.ui.tableWidget.setItem(row, col, cellinfo)
                col += 1
 
            row += 1
    def all(self):
        if self.flag==False:
            dynamic_row=len(self.all_data)
            self.flag=True
        else:
            dynamic_row=2
            self.flag=False
        self.init_UI(dynamic_row)
        #print(flag)
if __name__ == "__main__":
    app=QtWidgets.QApplication([])
    application = window()
    application.show()

    sys.exit(app.exec_())