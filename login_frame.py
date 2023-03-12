from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType

import sys , Database

# load the UI file
LoginUI,_ = loadUiType('login.ui')

# Local & Gloabl Variables
sqlite3 = Database.ConnectSqlite3()
loginStatus = 0
resetPasswordStatus = 0
userLoginID = 0

print("Welcome to the System. \nLoading...")

class Login(QFrame , LoginUI):

    # Constractor
    def __init__(self, parent=None):
        super(Login , self).__init__(parent)

        QFrame.__init__(self)
        
        self.setupUi(self)

        # Handle UI Changes
        self.UI_Changes()
        

        # Handle Buttons.
        self.handleButtons()



    # Load any changes in GUI
    def UI_Changes(self):
        # Clear window
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        QFrame.setWindowFlags(self,flags)
        QFrame.setAttribute(self,Qt.WA_TranslucentBackground)

        # Make a Shadwo
        self.label.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(234, 221, 185, 100)))
        self.label_2.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=0, yOffset=0, color=QColor(105, 118, 132, 100)))
        self.pushButton.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3, color=QColor(105, 118, 132, 100)))


    def handleButtons(self):
        
        self.pushButton.clicked.connect(self.loginBtn)
        self.pushButton_2.clicked.connect(self.ResetPasswordBtn)


    def checkLoginFields(self):
        usernameField = len( self.lineEdit.text() )
        passwordField = len( self.lineEdit_2.text() )

        empty = 0
        if usernameField==empty and passwordField==empty:
            print("Please enter a data first.")
            return False


        elif usernameField == empty:
            print("Please enter your Username.")
            return False

        
        elif passwordField ==  empty:
            print("Please enter your Password.")
            return False

        else:
            return True

    # Handle login
    def loginBtn(self):
        
        global loginStatus, userLoginID

        usernameField = self.lineEdit.text()
        passwordField = self.lineEdit_2.text()


        # Check my own username & password
        if usernameField=='admin' and passwordField=='000' and self.checkLoginFields()==True:

            #Insert data into database
            id = sqlite3.generateID("select * from login")
            userLoginID = id

            loginAsAdmin = True
            loginAsUser =False
            
            loginDbData = [(id, usernameField, passwordField, loginAsAdmin, loginAsUser)]
            sqlite3.insertManyData("insert into login values (?,?,?,?,?)",loginDbData)

            # Logine Complate.
            loginStatus = True
            
        elif self.checkLoginFields()==True :
            # Check data to login
            checkLoginData = sqlite3.getAll("select password, name from employee where name = '{}' and Password = '{}'".format(usernameField, passwordField))
            empty = 0

            loginAsAdmin = 0
            loginAsUser = 1

            if len( checkLoginData ) != empty :

                #Insert data into database
                id = sqlite3.generateID("select * from login")
                userLoginID = id


                sqlite3.insertManyData("insert into login values (?,?,?,?,?)",[
                    ( id, usernameField, passwordField, loginAsAdmin, loginAsUser)
                ])
                
                # Login Complate.
                loginStatus = True

            else:
                print("Wrong!!, username or password in incorrect!.")
  


        if loginStatus == True:
            qApp.quit()

        
    # Reset Password Button.
    def ResetPasswordBtn(self):
        global resetPasswordStatus
        resetPasswordStatus = True

        qApp.quit()

