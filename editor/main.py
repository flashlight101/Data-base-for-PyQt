#Дописать удаление элемента по нажатию клавиши delete или по кнопке
from PyQt5 import QtWidgets,Qt, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QCompleter, QVBoxLayout, QLineEdit, QCheckBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from editor.mainui import Ui_MainWindow
from PyQt5.QtGui import QPixmap
import PyQt5.QtGui
from PyQt5 import QtGui
import sys
import PySide2
import pyodbc
import re
from functools import partial
from editor.imagewindow import ImageWin
import regex as re
from editor.RangeSlider import QRangeSlider

import logging
# from editor.userwinui import Ui_Users
import time
'''class ImgWidget(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(ImgWidget, self).__init__(parent)
        pic = QPixmap(parent)
        self.setPixmap(pic)'''

# class UsersWin(QtWidgets.QDialog,Ui_Users):
#     def __init__(self,username):
#         super(UsersWin,self).__init__()

#         self.ui=Ui_Users()
#         self.ui.setupUi(self)
#         self.username=username
#         self.data = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',
#         SERVER='DESKTOP-775NG2O\MSSQLSERVER01',
#         DATABASE='anime',
#         trusted_connection='yes')#Подключение к базе данных
#         self.cursor = self.data.cursor()
#         self.init_ui()
    
#     def init_ui(self):
#         self.ui=Ui_Users()
#         self.ui.setupUi(self)
#         self.tablename="Users"
#         self.column = self.cursor.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME='"+str(self.tablename)+"'").fetchall()
#         self.all_data=self.cursor.execute("select * from Users").fetchall()
#         self.column=[elem[0] for elem in self.column]
#         self.ui.tableUsers.setColumnCount(len(self.column))
#         self.ui.tableUsers.setRowCount(5)
#         self.ui.tableUsers.setHorizontalHeaderLabels(self.column)
#         # self.ui.tableUsers.resizeColumnsToContents()
#         row=0
#         for tup in self.all_data:#Заполнение таблицы данными из БД
#             col = 0
#             for item in tup:
#                     self.cellinfo = QTableWidgetItem(str(item))
#                     self.ui.tableUsers.setItem(row, col, self.cellinfo)
#                     col += 1    
#             row += 1
#         self.ui.tableUsers.cellChanged.connect(self.modifying_table)
#         self.ui.deletebutton.clicked.connect(self.delbutton)
#     def delbutton(self):
#         insert="delete from users where id =(?)"
#         self.cursor.execute(insert,(self.ui.deleteusers.text()))
#         self.cursor.commit()
#     def modifying_table(self,row,col):
#         #Ошибка при изменении id
#         insert="update "+str(self.tablename)+" set "+str(self.column[col])+" = (?) where id = (?)"
#         self.cursor.execute(insert,(self.ui.tableUsers.item(row,col).text(),row+1))
#         self.cursor.commit()
#         self.log("update "+str(self.tablename)+" set "+str(self.column[col])+" = "+str(self.ui.tableUsers.item(row,col).text())+" where id = "+str(row+1)+"")
#     def log(self,sql):
#         tm = time.strftime("%Y-%m-%d %H:%M:%S")
#         insert = "INSERT INTO log ([log],[created_at],[user]) values (?,?,?)"
#         self.cursor.execute(insert,(sql,tm,self.username))
#         self.cursor.commit()









class window(QtWidgets.QMainWindow):
    def __init__(self,username):
        super(window,self).__init__()
        self.data = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',
        SERVER='DESKTOP-775NG2O\MSSQLSERVER01',
        DATABASE='anime',
        trusted_connection='yes')#Подключение к базе данных
        self.table_name='Characters'
        self.flag=False
        self.searchflag=True
        self.selectArray=[]
        self.selectle=[]
        self.username=username
        self.init_UI()
    def init_UI(self,dynamic_row=10):
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        #self.table_name='characters'
        self.ui.menuwidget.activated[str].connect(self.onChanged)
        self.cursor = self.data.cursor()
        sql="SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME='"+str(self.table_name)+"'"
        self.column = self.cursor.execute(sql).fetchall()
        # self.log(sql)
        if self.searchflag==True:
            if(self.table_name=='Characters'):
                self.all_data=self.cursor.execute("select characters.*,images.photo from characters left join images on characters.id=images.id").fetchall()
            else: 
                self.all_data=self.cursor.execute("select "+str(self.table_name)+".* from "+str(self.table_name)).fetchall()
        self.column=[elem[0] for elem in self.column]
        self.columnadditem=self.column.copy()
        if(self.table_name=='Characters'):
            self.column.append('photo')
            #self.columnadditem.append('photo')
        self.columnadditem.remove('id')
        print(self.columnadditem)
        #self.dynamic_row=2#len(data)
        self.ui.pushButton.clicked.connect(self.all)
        self.slider=QRangeSlider(self)
        self.slider.setGeometry(QtCore.QRect(1450, 350, 300, 40))
        self.slider.setRange(0,300)
        self.slider.setMax(300)
        self.massslider=QRangeSlider(self)
        self.massslider.setGeometry(QtCore.QRect(1450, 450, 300, 40))
        self.massslider.setRange(0,200)
        self.massslider.setMax(200)
        print(self.slider.endValueChanged)
        self.ui.search.clicked.connect(self.search)
        #Реализация подсказок
        # wordList=["select"," characters.*,","images.photo"," from ","characters ","left"," join"," images ","on ","characters.id=images.id"]
        wordList=self.loadDictionary()
        completer = QCompleter(wordList, self)
        completer.setCaseSensitivity(PyQt5.QtCore.Qt.CaseInsensitive)
        self.ui.searchline.setCompleter(completer)
        #Таблица для добавления данных в БД
        self.ui.additemwidget.setColumnCount(len(self.columnadditem))
        self.ui.additemwidget.setHorizontalHeaderLabels(self.columnadditem)
        self.ui.additemwidget.setRowCount(1)
        self.ui.additembutton.clicked.connect(self.additemdatabase)
        #Основная таблица
        self.ui.tableWidget.setColumnCount(len(self.column))
        self.ui.tableWidget.setRowCount(dynamic_row)
        self.ui.tableWidget.setHorizontalHeaderLabels(self.column)
        #self.ui.pushButton.clicked.connect(self.all)
        self.ui.tableWidget.setSortingEnabled(True)
        row = 0
        self.btn=[]
        self.ui.tableWidget.resizeColumnsToContents()
        #print(self.column)
        for tup in self.all_data:#Заполнение таблицы данными из БД
            col = 0
            for item in tup:
                if col==12:
                    self.btn.append(Qt.QPushButton("Открыть картинку"))
                    self.ui.tableWidget.setCellWidget(row, col, self.btn[row])
                    col += 1
                    #self.button=self.btn[row]
                    self.btn[row].clicked.connect(partial(self.open_image,row))#Открытие картинки в новом окне
                    #print(row)
                    #print(re.search(r"\\", str(item)))
                else:
                    self.cellinfo = QTableWidgetItem(str(item))
                    self.ui.tableWidget.setItem(row, col, self.cellinfo)
                    col += 1    
            row += 1
        #self.cellinfo.setFlags(self.cellinfo.flags() & ~QtCore.Qt.ItemIsEditable)
        self.searchflag=True
        self.ui.colorRed.stateChanged.connect(self.checkred)
        self.ui.colorBlue.stateChanged.connect(self.checkblue)
        self.ui.colorGreen.stateChanged.connect(self.checkgreen)
        self.ui.colorWhite.stateChanged.connect(self.checkwhite)
        self.ui.colorLight.stateChanged.connect(self.checklight)
        self.ui.colorYellow.stateChanged.connect(self.checkyellow)
        self.ui.colorBrown.stateChanged.connect(self.checkbrown)
        self.ui.colorDark.stateChanged.connect(self.checkdark)
        self.ui.colorOrange.stateChanged.connect(self.checkorange)
        self.ui.colorFair.stateChanged.connect(self.checkfair)
        self.ui.genderMale.stateChanged.connect(self.checkmale)
        self.ui.genderFemale.stateChanged.connect(self.checkfemale)
        # self.ui.userbutton.clicked.connect(self.openUsers)
        self.ui.deletebutton.clicked.connect(self.delbutton)
        header = self.ui.tableWidget.horizontalHeader()       
        #header.setSectionResizeMode(11, QtWidgets.QHeaderView.Stretch)
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.updatetable.clicked.connect(self.updatetable)
        self.ui.tableWidget.clicked.connect(self.clicked_table)
        self.ui.tableWidget.cellChanged.connect(self.modifying_table)
    def updatetable(self):
        self.init_UI()
    def log(self,sql):
        tm = time.strftime("%Y-%m-%d %H:%M:%S")
        insert = "INSERT INTO log ([log],[created_at],[user]) values (?,?,?)"
        self.cursor.execute(insert,(sql,tm,self.username))
        self.cursor.commit()
    def delbutton(self):
        insert="delete from "+str(self.table_name)+" where id =(?)"
        self.cursor.execute(insert,(self.ui.deleteusers.text()))
        self.cursor.commit()
    # def openUsers(self):
    #     self.diff_window = UsersWin(self.username)
    #     self.diff_window.setWindowTitle('Новое окно')
    #     self.diff_window.show()
    def checkred(self,state):
        if state:
            self.selectArray.append("red")
        else:
            self.selectArray.remove("red")

    def checkblue(self,state):
        if state:
            self.selectArray.append("blue")
        else:
            self.selectArray.remove("blue")
    
    def checkgreen(self,state):
        if state:
            self.selectArray.append("green")
        else:
            self.selectArray.remove("green")
        
    def checkwhite(self,state):
        if state:
            self.selectArray.append("white")
        else:
            self.selectArray.remove("white")

    def checklight(self,state):
        if state:
            self.selectArray.append("light")
        else:
            self.selectArray.remove("light")

    def checkyellow(self,state):
        if state:
            self.selectArray.append("yellow")
        else:
            self.selectArray.remove("yellow")

    def checkbrown(self,state):
        if state:
            self.selectArray.append("brown")
        else:
            self.selectArray.remove("brown")

    def checkdark(self,state):
        if state:
            self.selectArray.append("dark")
        else:
            self.selectArray.remove("dark")

    def checkorange(self,state):
        if state:
            self.selectArray.append("orange")
        else:
            self.selectArray.remove("orange")

    def checkfair(self,state):
        if state:
            self.selectArray.append("fair")
        else:
            self.selectArray.remove("fair")


    def checkmale(self,state):
        if state:
            self.selectle.append("male")
        else:
            self.selectle.remove("male")

    def checkfemale(self,state):
        if state:
            self.selectle.append("female")
        else:
            self.selectle.remove("female")
    def search(self):
        insert=''
        insert="Select characters.*,images.photo From characters left join images on characters.id=images.id Where height between "+str(self.slider.start())+" and "+str(self.slider.end())+" and mass between "+str(self.massslider.start())+" and "+str(self.massslider.end())+" and CONCAT(name,skin_color,eye_color,hair_color,birth_year,homeworld,species,description) like '%"+str(self.ui.searchline.text())+"%'"
        if self.selectArray != []:
            for i in self.selectArray:
                print(i)
                insert+="and CONCAT(skin_color,eye_color,hair_color) like '%"+str(i)+"%'"
        if self.selectle != []:
            for i in self.selectle:
                insert+="and gender like '%"+str(i)+"%'"
        self.log(insert)
        self.all_data=self.cursor.execute(insert).fetchall()
        # and CONCAT(skin_color,eye_color,hair_color) like 'dark%'
        self.searchflag=False
        self.init_UI()

        
    def loadDictionary(self):#Загрузка столбцов из базы данных для отображения в виде подсказок
        wordList=[]
        insert="select name, hair_color, skin_color, eye_color, homeworld, species from characters"
        wordList+=self.cursor.execute(insert).fetchall()
        insert="select name, climate, terrain from planets"
        wordList+=self.cursor.execute(insert).fetchall()
        insert="select name, classification, designation, hair_colors, skin_colors, eye_colors, language, homeworld  from species"
        wordList+=self.cursor.execute(insert).fetchall()
        reg = re.compile('\'*\'')
        # wordList=set(self.strclean(",".join(str(x) for x in wordList)).split(', '))
        wordList=",".join(str(x) for x in wordList)
        wordList=reg.sub('', wordList)
        wordList=self.strmodify(wordList).split(',')
        wordList=[x.strip(' ') for x in wordList]
        return set(wordList)
    def strclean(self,string):#Очищение строки для подачи в БД
        badchar=['[',']','(',')',' ']
        for i in badchar : 
            string = string.replace(i, '')
        return string 
    def strmodify(self,string):#Очищение строки для подачи в БД
        badchar=['\'','[',']','(',')']
        for i in badchar : 
            string = string.replace(i, '')
        return string 
    def additemdatabase(self):#Добавление записи в базу данных 
        print("govno")
        data=[]
        for i in range(len(self.columnadditem)):
            try:
                data.append(str(self.ui.additemwidget.item(0,i).text()))
            except:
                data.append(None)
        insert="insert into "+str(self.table_name)+"("+self.strmodify(str(self.columnadditem))+") values(?,?,?,?,?,?,?,?,?,?)"#Дописать добавление в БД
        self.cursor.execute(insert,(data))
        self.cursor.commit()
    def onChanged(self,text):#Выбор таблицы, дописать изменение в графе выбора
        self.table_name=text
        self.ui.menuwidget.setItemText(0,text)
        self.show()
        self.init_UI()

    def clicked_table(self):
        rows = sorted(set(index.row() for index in
                      self.ui.tableWidget.selectedIndexes()))
        for row in rows:
            self.cellinfo.setFlags(self.cellinfo.flags() & ~QtCore.Qt.ItemIsEditable)
            self.cellinfo.setFlags(self.cellinfo.flags() & ~QtCore.Qt.ItemIsEditable)
            print('Row %d is selected' % row)

    def open_image(self,id):#Открытие картинки в новом окне
        self.ui.imagewindow = ImageWin(id+1)
        self.ui.imagewindow.show()
    def all(self):#Реализация кнопки, которая реализует функцию "Показать больше/меньше данных"
        if self.flag==False:
            dynamic_row=len(self.all_data)
            self.flag=True
        else:
            dynamic_row=10
            self.flag=False
        self.init_UI(dynamic_row)
        #print(flag)
    
    def modifying_table(self,row,col):
        #Ошибка при изменении id
        insert="update "+str(self.table_name)+" set "+str(self.column[col])+" = (?) where id = (?)"
        print(self.ui.tableWidget.item(row,col).text())
        print(row+1)
        self.cursor.execute(insert,(self.ui.tableWidget.item(row,col).text(),row+1))
        self.cursor.commit()
        self.log("update "+str(self.table_name)+" set "+str(self.column[col])+" = "+str(self.ui.tableWidget.item(row,col).text())+" where id = "+str(row+1)+"")
if __name__ == "__main__":
    app=QtWidgets.QApplication([])
    application = window()
    application.show()

    sys.exit(app.exec_())
#https://www.cyberforum.ru/python-graphics/thread2607193.html Редактирование ячейки
#https://issue.life/questions/54316791 удаление строки в таблице
#Спросить у Волковой, можно ли делать поиск по талице без использования sql