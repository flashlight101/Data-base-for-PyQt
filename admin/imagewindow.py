from PyQt5 import QtWidgets, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QLabel
from PySide2.QtGui import QPixmapCache
from admin.imagewindowui import Ui_Form
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
import base64 
import pyodbc
import os
import time
class ImageWin(QtWidgets.QDialog,Ui_Form):
    def __init__(self,id,username):
        super(ImageWin,self).__init__()
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        
        self.id=id#Принимаем id 
        self.data = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',
        SERVER='DESKTOP-775NG2O\MSSQLSERVER01',
        DATABASE='anime',
        trusted_connection='yes')#Подключение к базе данных
        self.cursor = self.data.cursor()
        self.username=username
        self.init_ui()

    def init_ui(self):
        print(self.id)
        try:
            self.item=self.cursor.execute("select photo from images where id = (?)",self.id).fetchall()
            self.item=[elem[0] for elem in self.item]
            self.item=self.item[0]
        except:
            insert="insert into images(id,Photo) values(?,?)"
            self.cursor.execute(insert,(self.id,None))
            self.cursor.commit()
        #print(self.item)
        if(self.item!=[]):
            imgdata = base64.b64decode(self.item)
            filename = 'some_image.jpg'
            with open(filename, 'wb') as f:
                f.write(imgdata)
            self.label = QLabel(self)
            pixmap = QPixmap('some_image.jpg')
            pixmap=pixmap.scaled(400, 400)
            self.label.setPixmap(pixmap)
            os.remove('some_image.jpg')
        else:
            self.label = QLabel(self)
            pixmap = QPixmap()
            pixmap=pixmap.scaled(400, 400)
            self.label.setPixmap(pixmap)
        self.ui.pushButton.clicked.connect(self.getFileName)
        
    def getFileName(self):
        self.filename = QFileDialog.getOpenFileName(self,
                             "Выбрать файл")
        image = open(str(self.filename[0]), 'rb') #open binary file in read mode
        image_read = image.read()
        self.image_64_encode = base64.encodestring(image_read)
        self.image_64_encode=pyodbc.Binary(self.image_64_encode)
        if (self.item == None):
            insert="insert into images(id,Photo) values(?,?)"
            self.cursor.execute(insert,(self.id,self.image_64_encode))
            self.cursor.commit()
            #self.log("insert into images(id,Photo) values("+str(self.id)+","+str(self.image_64_encode)+")")
        else:
            insert="update images set photo = (?) where id = (?)"
            self.cursor.execute(insert,(self.image_64_encode,self.id))
            self.cursor.commit()
           # self.log("update images set photo = ("+str(self.image_64_encode)+") where id = ("+str(self.id)+")")
        #self.cursor = self.data.cursor()
        #self.cursor.commit()
        #print(self.item[0])
        self.init_ui()
    def log(self,sql):
        tm = time.strftime("%Y-%m-%d %H:%M:%S")
        insert = "INSERT INTO log ([log],[created_at],[user]) values (?,?,?)"
        self.cursor.execute(insert,(sql,tm,self.username))
        self.cursor.commit()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    w = ImageWin()
    w.show()
    sys.exit(app.exec_())