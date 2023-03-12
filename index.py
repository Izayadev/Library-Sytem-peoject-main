from calendar import day_name
from csv import excel
from curses import window
from datetime import datetime
from distutils.log import error
from email.policy import EmailPolicy
from enum import EnumMeta
from pydoc import allmethods
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType

import sys , sqlite3 , Tools, login_frame, Database, TabWidget, ExcelFiles, DateFile, random
# from xlsxwriter import *


MainUI,_ = loadUiType('main.ui')
""" Handle Classes"""
hpTool = TabWidget.DailyMovment()
helpTool = TabWidget


database = Database.ConnectSqlite3()
print("Connected to Database.")

""" Gloabl Variable"""
empty = 0 # to use in if statements.
adminAccess = 0
resetPasswordAccess = 0

# employee_id & branch_id for history ,check database
employee_id = 'admin'
branch_id = 'admin'

# Default Image for Book
default_book_image = 'wBook.png'
systemImage = "bg.jpeg"
use_book = 1


class Main(QMainWindow , MainUI):

    # The Constractor.
    def __init__(self, parent=None):
        super(Main , self).__init__(parent)

        QMainWindow.__init__(self)
        
        self.setupUi(self)
        self.UI_Changes()
        self.Handle_Buttons()

        
        # Set Visibale Tabs
        self.tabWidget_2.setTabVisible(1,0)
        self.tabWidget_2.setTabVisible(2,0)

        self.tabWidget_3.setTabVisible(1,0)
        self.tabWidget_3.setTabVisible(2,0)

        self.tabWidget_4.setTabVisible(2,0)
        self.tabWidget_4.setTabVisible(3,0)
        self.tabWidget_4.setTabVisible(1,0)

        # Load Data To ComboBoxies
        self.Show_All_Categories()
        self.Show_All_Publishers()
        self.Show_All_Authors()
        self.Show_Employee()
        

        # Login
        if login_frame.resetPasswordStatus == False:
            self.Handle_Login()

        else:
            self.Open_Reset_Password_Tap()
        


    # Handling GUI changes.
    def UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)
        
    def prt(self):
        print("YEss")

    def prt2(self):
        print("YEssaa")


    # Call the Buutons in one Group to Load them in system
    def Handle_Buttons(self):

        
       

        # Open Taps Buttons
        self.pushButton_54.clicked.connect(self.OpenProfileTab)
        self.pushButton_21.clicked.connect(self.LogoutSystem)
        self.pushButton.clicked.connect(self.Open_Daily_Movment_Tap)
        self.pushButton_2.clicked.connect(self.Open_Books_Tap)
        self.pushButton_6.clicked.connect(self.Open_Clients_Tap)
        self.pushButton_5.clicked.connect(self.Open_Dashboard_Tap)
        self.pushButton_4.clicked.connect(self.Open_History_Tap)
        self.pushButton_3.clicked.connect(self.Open_Reports_Tap)
        self.pushButton_7.clicked.connect(self.Open_Settings_Tap)

        # Reset Password Buttons 
        self.pushButton_getCodePassword_forgetPassword.clicked.connect(self.Handle_Reset_Password)


        #### Daily Movemnet Buttons
        self.pushButton_23.clicked.connect(self.getDilyTabSearch)
        self.pushButton_37.clicked.connect(self.getOrder)
        self.pushButton_8.clicked.connect(self.commitBookOrder)
        self.pushButton_9.clicked.connect(self.getBookPrice)

        #### Books Tap's Buttons
        self.pushButton_13.clicked.connect(self.Add_New_Book)
        self.pushButton_14.clicked.connect(self.Edit_Book_Search)
        self.pushButton_15.clicked.connect(self.Save_Edit_Book)
        self.pushButton_16.clicked.connect(self.Delete_Book)
        self.pushButton_10.clicked.connect(self.Book_filter_Search)
        self.pushButton_11.clicked.connect(self.Book_Export_Report)
        
        



        #### Clients Tap's Buttons
        self.pushButton_27.clicked.connect(self.Add_New_Client)
        self.pushButton_26.clicked.connect(self.SearchAboutClient)
        self.pushButton_28.clicked.connect(self.Edit_Client_Search)
        self.pushButton_29.clicked.connect(self.Save_Edit_Client)
        self.pushButton_30.clicked.connect(self.Delete_Client)
        self.pushButton_45.clicked.connect(self.ExportListOfClients)

        # Dashbourd Buttons
        self.pushButton_53.clicked.connect(self.chooseImageForBranch)

        # History Buttons.
        self.pushButton_33.clicked.connect(self.searchInHistory)
        self.pushButton_47.clicked.connect(self.ExportListOfActions)
        
        

        """===== Settings Buttons ====="""
        # Setting [All Data] Buttons
        self.pushButton_24.clicked.connect(self.Add_Branch)
        self.pushButton_25.clicked.connect(self.Add_Publisher)
        self.pushButton_31.clicked.connect(self.Add_Author)
        self.pushButton_32.clicked.connect(self.Add_Category)

        # Employeies tap's buttons
        self.pushButton_38.clicked.connect(self.Add_Employee)
        self.pushButton_36.clicked.connect(self.Check_Employee_toEdit)
        self.pushButton_56.clicked.connect(self.CommitEmployeeEdit) 
        self.pushButton_40.clicked.connect(self.Edit_Employee_Permissions) 
        self.pushButton_39.clicked.connect(self.Check_empployee_Permissions)
        self.pushButton_41.clicked.connect(self.Open_Reset_Password_Tap)

        # Admin Reports Buttons.
        self.pushButton_48.clicked.connect(self.Admin_Report)
        

        #### Reports Buttons 
        self.pushButton_49.clicked.connect(self.ExportReportOfBooks) 
        self.pushButton_50.clicked.connect(self.ExportReportAboutClients)
        self.pushButton_51.clicked.connect(self.ExportReportAboutEmployeies)

        # Open Image
        self.pushButton_17.clicked.connect(self.getImage)
           

    # Enabel ALL the permissions in the system.
    def adminPermissions(self):
        # Side Buttons
        self.pushButton_2.setEnabled(1)
        self.pushButton_6.setEnabled(1)
        self.pushButton_5.setEnabled(1)
        self.pushButton_4.setEnabled(1)
        self.pushButton_3.setEnabled(1)
        self.pushButton_7.setEnabled(1)

        # Book's tap buttons
        self.tabWidget_2.setTabVisible(1,1) # Add new book
        self.tabWidget_2.setTabVisible(2,1) # edit or delete book
        self.pushButton_11.setEnabled(1)
        self.pushButton_12.setEnabled(1)
        # self.pushButton_14.setEnabled(1)
        self.pushButton_15.setEnabled(1)
        self.pushButton_16.setEnabled(1)

        # Client's tap buttons
        self.tabWidget_3.setTabVisible(1,1) # Add new client
        self.tabWidget_3.setTabVisible(2,1) # edit or delete client
        # self.pushButton_26.setEnabled(1)
        self.pushButton_44.setEnabled(1)
        self.pushButton_45.setEnabled(1)
        self.pushButton_27.setEnabled(1)
        # self.pushButton_28.setEnabled(1)
        self.pushButton_29.setEnabled(1)
        self.pushButton_30.setEnabled(1)

        # Settings's tap buttons
        self.tabWidget_4.setTabVisible(1,1) # Add new employee
        self.tabWidget_4.setTabVisible(2,1) # permissions
        self.tabWidget_4.setTabVisible(3,1) # reports
        self.pushButton_25.setEnabled(1)
        self.pushButton_24.setEnabled(1)
        self.pushButton_31.setEnabled(1)
        self.pushButton_32.setEnabled(1)
        self.pushButton_36.setEnabled(1)
        self.pushButton_41.setEnabled(1)
        self.pushButton_38.setEnabled(1)

    # Get employee permissions from database, and return it.
    def getEmployeePermissions(self, username):
        # Get permissions from database
        employeePermissions = database.getOne("select * from employee_permission where name = '{}'".format(username))

        thePermissions = {
            'name':employeePermissions[1], 
            'add_book':employeePermissions[2], 'edit_book':employeePermissions[3], 'delete_book':employeePermissions[4], 'export_book':employeePermissions[5], 'import_book':employeePermissions[6],
            'add_client':employeePermissions[7], 'edit_client':employeePermissions[8], 'delete_client':employeePermissions[9], 'export_client':employeePermissions[10], 'import_client':employeePermissions[11],
            'book_tap':employeePermissions[12], 'client_tap':employeePermissions[13], 'dashbuord_tap':employeePermissions[14], 'history_tap':employeePermissions[15], 'reports_tap':employeePermissions[16], 'setting_tap':employeePermissions[17],
            'add_data':employeePermissions[18], 'add_employee':employeePermissions[19], 'edit_employee':employeePermissions[20],
            'admin':employeePermissions[21]
        }

        return thePermissions


    # Handle loginning and work with login_fram data and GUI.
    def Handle_Login(self):
        
        # Get Login_frame data Form database
        loginUiData = database.getOne("select username, password, its_me, error from login where id = {}".format(login_frame.userLoginID))
        
        # Get data from fields
        loginUiUsername = 0; loginUipassword = 1; loginUiIts_me=2; loginUiError=3;
        
        username  = loginUiData[loginUiUsername]
        password  = loginUiData[loginUipassword]
        
        loginAsAdmin = loginUiData[loginUiIts_me]
        loginAsUser= loginUiData[loginUiError]



        

        # Loginning as Admin.
        if username=='admin' and password=='000':
            print("Logining... --> username is Admin")

        else: # Loginning as an Employee
            # Check username and password data in database.
            employeeLoginData = database.getOne("select name, Branch from employee where name = '{}' and Password = '{}'".format(username, password))
            empty = 0

            if len( employeeLoginData ) != empty:
                
                # Get employee_id & branch
                global employee_id, branch_id

                employee_id = employeeLoginData[0]
                branch_id = employeeLoginData[1]
                branch_id = database.getOne("select name from branch where code = {}".format(branch_id))[0]
            
                # Get permissions from database
                employeePermissions = self.getEmployeePermissions(username)

                print("Loginnig... --> username is {}".format(username))
                print("Welcome {} to Branch {}".format(employee_id, branch_id))



            else:
                print("=========== WRONG!! ============= \npassword or username is incorrect.")


        # Enable Permissions Acces
        if loginAsAdmin == True: # just my own user UwU
            print("Welcome Admin... \nWait to set the permissions.")
            print("Ready to get Data...")
            
            # Admin -> All permissions
            self.adminPermissions()            

            # Open Today tap
            self.Open_Daily_Movment_Tap()

        elif loginAsUser == True: # --> Login as employee

            print("Mr {}... wait to set the permissions.".format(username))
            print("Ready to get Data...")


            if employeePermissions['admin']==True: # Admin -> All permissions
                self.adminPermissions()

            # Book tap permissions
            if employeePermissions['book_tap']==True: 
                self.pushButton_2.setEnabled(1)

                if employeePermissions['export_book'] == True:# Check Export  
                    self.pushButton_11.setEnabled(1)
                if employeePermissions['import_book'] == True: # Check Import
                    self.pushButton_12.setEnabled(1)


                if employeePermissions['add_book'] == True:# Check Add Book
                    self.tabWidget_2.setTabVisible(1,1)
                
                if employeePermissions['edit_book'] == True :# Check Edit Book
                    self.tabWidget_2.setTabVisible(2,1)
                    self.pushButton_15.setEnabled(1)
                    
                    if employeePermissions['delete_book'] == True : # Check delete book
                        self.pushButton_16.setEnabled(1)

            # Client tap permissions
            if employeePermissions['client_tap'] == True : 
                self.pushButton_6.setEnabled(1)

                if employeePermissions['export_client'] == True :# Check Export  
                    self.pushButton_45.setEnabled(1)
                if employeePermissions['import_client'] == True : # Check Import
                    self.pushButton_44.setEnabled(1)


                if employeePermissions['add_client'] == True :# Check Add Client
                    self.tabWidget_3.setTabVisible(1,1)
                
                if employeePermissions['edit_client'] == True :# Check Edit Client
                    self.tabWidget_3.setTabVisible(2,1)
                    self.pushButton_29.setEnabled(1)
                    
                    if employeePermissions['delete_client'] == True : # Check delete Client
                        self.pushButton_30.setEnabled(1)
                        
            # Dashbourd tab permissions
            if employeePermissions['dashbuord_tap'] == True :
                self.pushButton_5.setEnabled(1)
            
            # History tab permissions
            if employeePermissions['history_tap'] == True :
                self.pushButton_4.setEnabled(1)

            # Reports tab permissions
            if employeePermissions['reports_tap'] == True :
                self.pushButton_3.setEnabled(1)

            # Settings tab permissions
            if employeePermissions['setting_tap'] == True :
                self.pushButton_7.setEnabled(1)

                if employeePermissions['add_employee'] == True : # Add employee
                    self.tabWidget_4.setTabVisible(1,1)
                
                if employeePermissions['edit_employee'] == True : # Edit Employee
                    self.pushButton_36.setEnabled(1)
                    self.pushButton_41.setEnabled(1)

                if employeePermissions['add_data'] == True : # Add data
                    self.pushButton_24.setEnabled(1)
                    self.pushButton_25.setEnabled(1)
                    self.pushButton_31.setEnabled(1)
                    self.pushButton_32.setEnabled(1)
                
                if employeePermissions['add_employee'] == True : # Add employee
                    self.tabWidget_4.setTabVisible(1,1)
                else:
                    self.tabWidget_4.setTabVisible(1,0)


                    
                    
                
                if employeePermissions['edit_employee'] == True : # edit employee
                    self.tabWidget_4.setTabVisible(2,1)
                else:
                    self.tabWidget_4.setTabVisible(2,0)

                
            # Add this Aciotn in History
            history_id = database.generateID("select * from history")
            dateFromSystem = datetime.now().strftime('%d-%m-%Y %H:%M')
            
            database.insertManyData("insert into history values(?,?,?,?,?,?)",[
                (history_id, employee_id, 'Login', dateFromSystem, branch_id, username)
            ])
            
            
            # Open Today tap
            self.Open_Daily_Movment_Tap()

        
    # Handle reset employee password.
    def Handle_Reset_Password(self):
        canRun = True

        # Variables.
        employeeName = self.comboBox_selectEmployee_forgetPassword.currentText()
        adminPassword = self.lineEdit_writeAdminPassword_forgetPassword.text()
        label = self.label_getNewPassword_forgetPassword
        newPassword = 0

        # Check
        fields = {'admin password':adminPassword}
        isFieldsEmpty = Tools.checkFields(fields)

        if isFieldsEmpty==empty :
            canRun = False

        # Run.
        if canRun==True and adminPassword=='000':

            newPassword = Tools.getNewPassword(employeeName)
            
            if newPassword==empty:
                "There is no employee with this name '{}'".format(employeeName)
            else:

                # Save.
                actions = {'action':'edit employee password',
                           'extra':employeeName,
                           'branch id':branch_id,
                           'employee id':employee_id}
                Tools.SaveActionToHistory(actions)
                database.updateData("update employee set Password = {} where name = '{}'".format(newPassword, employeeName))

                # Notification.
                print("The new password is {}".format(newPassword))
                msg = "The new password is {}\nNow restart the system".format(newPassword)
                label.setText(msg)

                

                
        else:
            print("Admin Password Wrong!!")

                

    """==================================================================================
    ========================= Today tab's functions =================================="""
    
    """Dailymovments tab"""
    # Search
    # Workable
    def getDilyTabSearch(self): # Work with DB --> daily_movments table.
        
        # VARIABLES
        searchText = self.lineEdit_59.text()
        table = self.tableWidget_2

        # DATA
        thisData = {'search text':searchText, 'table':table}
        
        
        # CHECK
        if len(searchText) != empty:
            
            # PROSSES
            hpTool.getDailyBooksSearch(thisData)

        # OUTPUT

    """Order a Book, tab"""
    def getOrder(self):

        searchText = self.lineEdit_60
        label = self.lineEdit_4
        price = self.label_67
        
        table = self.tableWidget_4
        tab = self.TaodayWidget

        thisData = {'search text':searchText, 'table':table, 'tab':tab, 'label':label, 'price':price}
        hpTool.getOrderTabSearch(thisData)
        

    

    # Check and Get the Price.
    def getBookPrice(self):

        bookName = self.lineEdit_4.text()

        if len(bookName)==empty:
            print("Please Book title cannot be empty!")
        
        else:
        
            price = hpTool.getBookPrice(bookName)
            txt = "The Price : "+str(price)+"$"+"\nNote: Rent fee is 2$"
            self.label_67.setText(txt)
            return price
            
    # Workable
    def commitBookOrder(self): # Wrok with GUI --> Commit Order Tab.

        # GET DATA
        bookTitle = self.lineEdit_4.text()
        clientID = self.lineEdit_7.text()
        orderType = self.comboBox

        label = self.label_21

        # SORD DATA
        thisData = {'employee id':employee_id, 'branch id':branch_id,
        'book title':bookTitle, 'client id':clientID, 
        'order type':orderType, 'label':label}

        # CHECK
        thisFields = {'book title':bookTitle, 'client id':clientID}
        checkResult = Tools.checkFields(thisFields)
        
        if checkResult != empty:

            hpTool.getOrderDetails(thisData)

            

        # REFRASH
        tableName = self.tableWidget_2
        hpTool.showDailyBooks({'table':tableName})


    """===========================================================================
    ======================== Book tab's functions ============================="""

    # Book tap filter to search in database
    def Book_filter_Search(self):

        # VARIABLES
        searchText = self.lineEdit_5.text()
        table = self.tableWidget_3
        thisData = {'search text':searchText, 'table':table, 'branch id':branch_id}

        # RUN
        helpTool.BookTab().searchAboutBook(thisData)
    

    # Show the Books in The Table.
    def Show_All_Books(self):

        # VARIABLES
        thisData = {'branch id':branch_id, 'table':self.tableWidget_3, 'tab':self.tabWidget_2, 'text':self.lineEdit_8}     

        # RUN
        helpTool.BookTab().getAllBooks(thisData)

        
            


        


    # Open a Dialog Window and Get Pecture for Books or a Profile
    def getImage(self):
        global use_book , img_name
        # Default image
        # default_image = '/home/izy/Desktop/Library System/wBook.png'
        # self.pixmap = QPixmap(default_image)

        # Open Dialog and Get Picture
        img_name = QFileDialog.getOpenFileName(self, "Get the Image", "/home/izy/Desktop/Library System", "All Files (*);;PNG Files (*.png)")
        QFileDialog.getOpenFileName()
        # Open The Image this run
        print(img_name)
        self.pixmap = QPixmap(img_name[0])

        # Add Image to Label
        self.label_19.setPixmap(self.pixmap)

        # Change use_book variable statue
        use_book = 0


    # Add New Book to Database
    def Add_New_Book(self):
         
        # Get Data from GUI [Fields]
        bookTitle = self.lineEdit_6.text() 
        bookPrice = self.lineEdit_11.text()

        bookPart = self.lineEdit_50.text()
        bookDescription = self.textEdit.toPlainText()

        bookCategory = self.comboBox_4.currentText()
        bookPublisher = self.comboBox_8.currentText()
        
        bookAuthor = self.comboBox_6.currentText()
        bookStatus = self.comboBox_7.currentText()

        bookCode = str( self.comboBox_4.currentIndex() ) +'0'+ str( random.randint(111, 999) )
        bookBarcode = "249"+str(random.randint(111111, 999999))
        bookQuantity = self.lineEdit_54.text()

        # Get the Image
        if use_book==1 : # User didnt add a picture

            # Get image path
            bookImage = default_book_image

        else : # User Add a picture

            # Get image path
            bookImage = img_name[0]
        

        # Sort data
        thisData = {
            'title':bookTitle, 'description':bookDescription, 'author':bookAuthor,
            'category':bookCategory, 'publisher':bookPublisher, 'part':bookPart,
            'price':bookPrice, 'code':bookCode, 'barcode':bookBarcode,
            'status':bookStatus, 'quantity':bookQuantity, 'image':bookImage,
            'branch id':branch_id, 'employee id':employee_id
        }

        # RUN
        helpTool.BookTab().submitNewBook(thisData)


        # REFRESH
        self.Show_All_Books()

        # Clear Fields
        self.lineEdit_6.clear()
        self.lineEdit_11.clear()
        self.lineEdit_50.clear()
        self.textEdit.clear()
        self.lineEdit_54.clear()
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_8.setCurrentIndex(0)
        self.comboBox_6.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        


    # Edit a Book and svae changes in database
    def Edit_Book_Search(self):
        
        
        # Sort data.
        bookTitle = self.lineEdit_9.text()

        thisData = {'branch id':branch_id, 'book search':self.lineEdit_8, 'book title':self.lineEdit_9,
        'book description':self.textEdit_3, 'book category':self.comboBox_5,
        'book price':self.lineEdit_48, "book code":self.lineEdit_12,
        "book publisher":self.comboBox_13, "book author":self.comboBox_10,
        "book part":self.lineEdit_51, "book quantity":self.lineEdit_55, 'book status':self.comboBox_12,
        'book image':self.label_20, 'pixmap':self.pixmap}
            
        # RUN
        helpTool.BookTab().submitEditBook(thisData)


    # Save Changes from Edit Book in database
    def Save_Edit_Book(self):
        
        TabWidget.BookTab().submitChange()
        # Notification
        self.statusBar().showMessage("Edited !!") # Notification

    # Delete a Book and Save th Changes in Database
    def Delete_Book(self):

        # action, extra, branch id, employee id
        # submitDeleteBook
        # VARIABLES
        code = self.lineEdit_8.text() # Get a code to search via 
        thisData = {'branch id':branch_id, 'employee id':employee_id, 'code':code}

        # RUN
        TabWidget.BookTab().submitDeleteBook(thisData)

        # Refreash Data
        self.Show_All_Books()


        # Clear fields
        self.lineEdit_9.clear()
        self.textEdit_3.clear()
        self.lineEdit_48.clear()
        self.lineEdit_12.clear()
        self.lineEdit_51.clear()

        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_13.setCurrentIndex(0)
        self.comboBox_10.setCurrentIndex(0)
        self.comboBox_12.setCurrentIndex(0)


        # Notification
        self.statusBar().showMessage("Deleted !!") # Notification

        # Refreash Data
        self.Show_All_Books()


    # This to export a list of books which in the screen in gui.
    def Book_Export_Report(self):
        """Export book's list to an Excel file."""

        # RUN
        ExcelFiles.BookReports().exportBookReport({'employee id':employee_id, 'branch id':branch_id})

        # NOTIFICATIONS
        print("Exported!")



    """==============================================================================
    ================================== Clients Tab Functions ==============================="""
    
    # Show data in client table
    def Show_All_Clients(self):
        
        # Variables
        tableName = self.tableWidget_5

        # Get Data from Database.
        clientsData = database.getAll("select name, mail, phone, national_id, date from clients")

        # Insert data into table
        Tools.showDataInTable(tableName, clientsData)
        
    # Add New Client & Save changes in database.
    def getClientDataFields(self): # Helpful tool
        """Get the fields's data from screen in tab add new client.\n
        return Dictionary of objects in this order\n
        <name, mail, phone, id>"""

        # Get Data from Fields
        client_name = self.lineEdit_13
        client_mail = self.lineEdit_14
        client_phone = self.lineEdit_16
        client_national_id = self.lineEdit_18

        return {'name':client_name, 'mail':client_mail, 'phone':client_phone, 'id':client_national_id}
        
    # Tool --> clean fields.    
    def clearClientFields(self): # Helpful tool
        """Clear the field from data in add new client tab."""
        # Clear Fields
        self.lineEdit_13.clear()
        self.lineEdit_14.clear()
        self.lineEdit_16.clear()
        self.lineEdit_18.clear()

    # Add new client to system.
    def Add_New_Client(self):
        """add new client in system."""
        # Variables.
        objectsName = self.getClientDataFields()
        cleintName = objectsName['name'].text()
        
        # Run
        runScript = TabWidget.ClientTab().addNewClient(objectsName)
        
        if runScript == True:

            # Save action to history
            if branch_id == adminAccess or employee_id == adminAccess:
                thisData = {'employee id':"Admin", 'branch id':"Admin", 'action':"Add new client", 'extra':cleintName} 
            else:
                thisData = {'employee id':employee_id, 'branch id':branch_id, 'action':"Add new client", 'extra':cleintName} 

            Tools.SaveActionToHistory(thisData)
           

            # Notification.
            self.statusBar().showMessage("Clinet {} added Successfuly !!".format(cleintName))

            # Clean Screen.
            self.clearClientFields()

        # Refreash.
        self.Show_All_Clients()

    # Hanlde Search Bar.
    def SearchAboutClient(self):
        """Search by name, phone, mail, or id"""

        # GET Search Text.
        searchText = self.lineEdit_46.text()
        table = self.tableWidget_5

        # Run 
        TabWidget.ClientTab().getSearchData({'search text':searchText, 'table':table})

        # Notification
        self.statusBar().showMessage("Data Loaded to Screen !!") 

    # Load data to Fields.
    def loadClientDataToEditsFields(self, clientData): # Tool
        """take a data then load id in their fields in edit clien tab."""
        # Variables and indexies.
        nameIndx = 0
        mailIndx = 1
        phoneIndx = 2
        idIndx = 3

        # Load data to fields
        clientName = self.lineEdit_17.setText(clientData[nameIndx])
        clientMail = self.lineEdit_15.setText(clientData[mailIndx])
        clientPhone = self.lineEdit_20.setText(clientData[phoneIndx])
        clientID = self.lineEdit_19.setText(str(clientData[idIndx]))

        # Notification
        self.statusBar().showMessage("Client data loaded successfuly !!") 

    # Hable Search bar in Edit client Tab.
    def Edit_Client_Search(self):
        """Search about client by one if his data then load his data to be editable."""

        # Variables.
        searchText = self.lineEdit_21.text()
        run = True

        # Check Field.
        if Tools.checkFields({'search text':searchText}) == False:
            run = False
            

        # Run.
        if run == True:

            # Get data.
            clientData = TabWidget.ClientTab().loadCleintDataToEdit(searchText)

            # Load in Fields.
            if len(clientData) != empty:
                self.loadClientDataToEditsFields(clientData)



        # # Get Client data to search via
        # client_data = str(self.lineEdit_21.text()) # Here Data text what i will search via.

        # # Check is there last search !!
        # if ( len(self.lineEdit_17.text()) > 0 ) : # is not empty  --> Here i take client name feild to check
            
        #     # Clear Feilds
        #     self.lineEdit_17.clear() # name
        #     self.lineEdit_15.clear() # mail
        #     self.lineEdit_20.clear() # phone
        #     self.lineEdit_19.clear() # nationa ID

        
        # # Get filter search
        # filter = self.comboBox_37.currentIndex()
        # filter_name = ""

        # if filter == 0:
        #     filter_name = "name"

        # elif filter == 1:
        #     filter_name = "mail"
            
        # elif filter == 2:
        #     filter_name = "phone"

        # else:
        #     filter_name = "national_id"


        # # Check if client data dield is empty
        # if len(client_data) <= 0:
        #     print("Please Enter Client Data to Search !!") # Notification

        # else : # is not Empty

        #     # Search in database using filter code
        #     sql = "select * from clients where {0} = '{1}'" 
        #     sql = sql.format(filter_name, client_data)
        #     self.cur.execute(sql)

        #     data_lenghth = len( self.cur.fetchall() ) # how many data here

        #     if data_lenghth == 0 : # is it not in database
        #         self.statusBar().showMessage("There is no Client with this {} data !".format(client_data)) # Notification

        #     else : # if Founded
                
        #         sql = "select * from clients where {0} = '{1}'" 
        #         sql = sql.format(filter_name, client_data)
                
                
        #         self.cur.execute(sql)
        #         data = self.cur.fetchone()                 

        #         # Load data to fields
        #         client_name = self.lineEdit_17.setText(data[1])
        #         client_mail = self.lineEdit_15.setText(data[2])
        #         client_phone = self.lineEdit_20.setText(data[3])
        #         client_national_id = self.lineEdit_19.setText(str(data[5]))

        #         # Notification
        #         print("Search Done !!")

    # Tool --> get cleint's id.
    def getClientIdFromSearch(self,nationalID): # Tool
        """Get cleint id in database ans used in system."""

        id = database.getOne("select id from clients where national_id = {}".format(nationalID))

        return int(id[0])

    # Tool --> to get data from Fields in Edit client tab.
    def getEditableClientData(self): # Tool
        """Get Edits data from fields in edit client data tab.\n
        then return data as dictionary data type in this Keys order-->\n
        <id, name, mail, phone, national id>"""

        # __inti__
        canRun = True


        # Get Data from Fields
        clientName = self.lineEdit_17.text()
        clientMail = self.lineEdit_15.text()
        clientPhone = self.lineEdit_20.text()
        clientID = self.lineEdit_19.text()

        # Check 
        checkResult = Tools.checkFields({'client name':clientName,
                           'client mail':clientMail,
                           'client phone':clientPhone,
                           'client id':clientID})
        if checkResult == False:
            canRun = False
        
        # Run.
        if canRun==True:
            id = self.getClientIdFromSearch(clientID)

            # Return.
            return {'id':id, 'name':clientName, 'mail':clientMail, 'phone':clientPhone, 'national id':int(clientID)}
        else:
            return {}
    
    # Commit changes in Edit Client tab.
    def Save_Edit_Client(self):
        """Submit and Save the changes."""
        # __inti__
        canRun = True

        # Variables.
        clientData = self.getEditableClientData()
        cleintName = clientData['name']

        
        # Check and Kick.
        if len(clientData) == empty:
            canRun = False

        # Run.
        if canRun == True:
            TabWidget.ClientTab().updateClientData(clientData)

            # Notification.
            self.statusBar().showMessage("Clinet {} updated successfuly !!".format(cleintName))

            # Save Action.
            if branch_id==adminAccess or employee_id==adminAccess:
                thisData = {'action':'update cleint', 'extra':cleintName, 'branch id':"admin", 'employee id':"admin"}
            
            else:
                thisData = {'action':'update cleint', 'extra':cleintName, 'branch id':branch_id, 'employee id':employee_id}
            
            Tools.SaveActionToHistory(thisData)
            
            # Refresh.
            self.Show_All_Clients()

    # Tool --> clean fields.
    def clearEditClientDataFields(self): # Tool
        """clear the fields from data in edit client tab."""

        # Now Clear Feilds
        self.lineEdit_17.clear()
        self.lineEdit_15.clear()
        self.lineEdit_20.clear()
        self.lineEdit_19.clear()
        self.lineEdit_21.clear()

    # Delete Client from System.
    def Delete_Client(self):
        """delete a cleint from database."""
        # __inti__
        canRun = True

        # Variables.
        clientData = self.getEditableClientData()
        id = clientData['id']
        cleintName = clientData['name']

        # Check and Kick.
        if len( clientData ) == empty:
            canRun = False
        
        # Run.
        if canRun==True:
            
            # Delete.
            database.deleteData("delete from clients where id = {}".format(id))

            # Save Action in History.
            if branch_id == adminAccess or employee_id == adminAccess:
                thisData = {'action':'delete client', 'extra':cleintName, 'branch id':"admin", 'employee id': "admin"}
            else:
                thisData = {'action':'delete client', 'extra':cleintName, 'branch id':branch_id, 'employee id': employee_id}
            
            Tools.SaveActionToHistory(thisData)

            # Notification.
            self.statusBar().showMessage("Clinet Deleted Successfuly !!")

            # Clean.
            
            self.clearEditClientDataFields()

        # Refreash.
        self.tableWidget_5.clearContents()
        self.Show_All_Clients()
        
        # # Get client id from database
        # client_data = str(self.lineEdit_21.text()) # Here Data text what i will search via.
        # name = self.lineEdit_17.text()

        # # Get filter search
        # filter = self.comboBox_37.currentIndex()
        # filter_name = ""

        # if filter == 0:
        #     filter_name = "name"

        # elif filter == 1:
        #     filter_name = "mail"
            
        # elif filter == 2:
        #     filter_name = "phone"

        # else:
        #     filter_name = "national_id"

        # self.cur.execute("select * from clients where {0} = '{1}'".format(filter_name, client_data))
        # id  = self.cur.fetchone()[0]


        # print(id)

        # # Now Delete it
        # self.cur.execute("delete from clients where id = '{}'".format(id))

        


        # # Add this Actions in History
        # # Generate History id
        # self.cur.execute("select * from history")
        # history_id = len( self.cur.fetchall() ) +1
        # date = datetime.now().strftime('%d-%m-%Y %H:%M')


        # # Check is There another id same and fix it
        # self.cur.execute("select * from books where id = '{}'".format(history_id))
        # count_id = len( self.cur.fetchall() )
        # client_name = self.lineEdit_17.text()

        
        # if count_id > 0:
        #     history_id+=1

        # self.cur.executemany("insert into history values (?,?,?,?,?,?)",[(
        #     history_id, employee_id, "Delete Client", date, branch_id, client_name
        # )])

        # # Save data in database
        # self.db.commit()

        # # Now Clear Feilds
        # client_name = self.lineEdit_17.clear()
        # client_mail = self.lineEdit_15.clear()
        # client_phone = self.lineEdit_20.clear()
        # client_national_id = self.lineEdit_19.clear()

        # client_data = self.lineEdit_21.clear()


        # # Now Show a Notifications
        # message = "The Cleint {} was deleted !".format(name)
        # print(message)
        # self.statusBar().showMessage(message)

    # Export List of The Clients in the System.
    def ExportListOfClients(self):
        """Export all clients in list to an excel file."""

        ExcelFiles.ClientReports().exportClientsList()
        print("exported!!")
       

    """======================================================================================
    ================================ Dashbourd Tab Functions ============================="""
    # Open a Dialog Window and choose Picture.
    def getPicture(self, pixmap, label):
        
        # Open Dialog and Get Picture
        imgName = QFileDialog.getOpenFileName(self, "Get the Image", "/home/izy/Desktop/Library System", "All Files (*);;PNG Files (*.png)")

        # Open The Image this run
        pixmap = QPixmap(imgName[0])

        # Add Image to Label
        label.setPixmap(pixmap)

        # Output.
        return imgName

    # Choose image.
    def chooseImageForBranch(self):

        # Variables.
        pixmap = self.pixmap
        label = self.label_97

        # Run.
        image = self.getPicture(pixmap, label)

        # Save.
        global systemImage
        systemImage = image

    # Load information data.
    def LoadSystemInformation(self):
        """get branch data ,  image , admin data, system data."""

        # Picture.
        self.pixmap = QPixmap(systemImage)
        self.label_97.setPixmap(self.pixmap)

        # Variables.
        thisObjects = {
            'branch':branch_id,
            'name':self.label_93,
            'location':self.label_90,
            'admin':self.label_95,
            'title':self.label_44,
            
            'rent':self.label_113,
            'retrieve':self.label_25,
            'total':self.label_26,
            'books':self.label_27,
            'clients':self.label_28,
            'visitors':self.label_29,
            'income':self.label_33,
            'outcome':self.label_42,
        }

        # Run.
        TabWidget.DashbourdTab().loadBranchData(thisObjects)
    """======================================================================================
    ================================ History Tab Functions ================================"""
    
    # Show the data from database to history tap in gui
    def Show_History(self):

        # Variables.
        table = self.tableWidget_6

        # Get data from database
        hitory = database.getAll("select employee, actions, branch_id, date, extra from history")

        # Insert data into table
        Tools.showDataInTable(table, hitory)

    # Search in history table.
    def searchInHistory(self):
        """Search in history table by employee, branch, action, date or extra."""
        # __inti__
        canRun = True

        # Variable.
        searchText = self.lineEdit_3.text()
        table = self.tableWidget_6

        # Check and Kick.
        if len(searchText) == empty:
            print("Please Enter a Data First.")
            canRun = False
        
        # Run.
        if canRun==True:
            TabWidget.HistoryTab().getSearchAboutText(searchText, table)

    # Export List of Action to Excel File.
    def ExportListOfActions(self):
        """Exported from history table to excel file."""

        # Run.
        ExcelFiles.HistoryReports().exportList()

        # Notification.
        print("Exported.")










    """===============================================================================================
    ============================= Reports Tab Functions."""
    
    # Book tab --> show a report about books in the system
    def Show_All_Book_Reports(self):

        # Variables.
        table = self.tableWidget_7

        # Run.
        TabWidget.ReportsTab().getBookReport(table)

    # Export an Excel file about All Books in The System.
    def ExportReportOfBooks(self):
        """Export a Report of All Books in The System."""

        # Run.
        ExcelFiles.ReportsTab().exportBooksReport()


    # Client tab --> Show a Report about Client in The System.    
    def Show_All_Client_Reports(self):
        """Export as Excel File Data is the All Client in the System."""

        # Variables.
        table = self.tableWidget_8
        
        # Run.
        TabWidget.ReportsTab().getClientsReport(table)      

    # Export a list of Clients Report.
    def ExportReportAboutClients(self):
        """Export a List of Clients Report as Excel File."""

        # Run.
        ExcelFiles.ReportsTab().exportClientsReport()

    # Employee tab --> Show A Report about Employeies in The System.
    def Show_Employee_Report(self):
        # Employee tab --> Show A Report about Employeies in The System.
        
        # Variables.
        table = self.tableWidget_10

        # Run.
        TabWidget.ReportsTab().getEmployeiesReport(table)


    # Export a list of Employeis Report.
    def ExportReportAboutEmployeies(self):
        """Export a list of Employeis Report as Excel File."""
        
        # Variables.
        table = self.tableWidget_10
        
        # Run.
        tableData = Tools.getEmployeeTableWidgetData(table)
        ExcelFiles.ReportsTab().exportEmployeiesReport(tableData)

        # Notification.
        print("Exported!!")

    


    """==============================================================================
    ============================== Load Combo Box Data ==========================="""
    def Show_All_Categories(self):
        # Clear Trash
        self.comboBox_25.clear() 
        self.comboBox_25.addItem("---------")

        self.comboBox_4.clear() 
        self.comboBox_4.addItem("---------")

        self.comboBox_5.clear() 
        self.comboBox_5.addItem("---------")

        # Get Data from Database
        categories = database.getAll("select category_name from category")
        
        # Insert Data
        for category in categories:
            self.comboBox_25.addItem(category[0])
            self.comboBox_4.addItem(category[0])
            self.comboBox_5.addItem(category[0])

    def Show_All_Publishers(self):
        # Clear Trash
        self.comboBox_8.clear() 
        self.comboBox_8.addItem("---------")

        self.comboBox_13.clear() 
        self.comboBox_13.addItem("---------")
        

        # Get Data from Database
        publishers = database.getAll("select name from publisher") 

        # Insert Data
        for publisher in publishers:
            self.comboBox_8.addItem(publisher[0])
            self.comboBox_13.addItem(publisher[0])

    def Show_All_Authors(self):
        # Clear Trash
        self.comboBox_6.clear() 
        self.comboBox_6.addItem("---------")

        self.comboBox_10.clear() 
        self.comboBox_10.addItem("---------")
        

        # Get Data from Database
        publishers = database.getAll("select name from author")

        # Insert Data
        for publisher in publishers:
            self.comboBox_6.addItem(publisher[0])
            self.comboBox_10.addItem(publisher[0])

            



            

    """=============================================================================
    ============================== Setting Tab Functions. ======================="""
    
    """===== Branch ====="""
    # Get Branch Fields Data.
    def getBranchDataFields(self):
        # Get Branch Data from Fields.

        id = database.generateID("select * from branch")
        branchName = self.lineEdit_23.text()
        branchCode = self.lineEdit_24.text()
        branchLocation = self.lineEdit_25.text()
        branchAdmin = self.lineEdit_39.text()

        # Check and Kick.
        fields = {'branch name':branchName, 'branch code':branchCode, 'branch location':branchLocation, 'branch admin':branchAdmin}
        checkResult = Tools.checkFields(fields)

        if checkResult==True:
            return (id, branchName, branchCode, branchLocation, branchAdmin)
        else:
            return checkResult
    
    
    # Clean.
    def clearBranchDataFields(self):
        # Cleart Fields
        self.lineEdit_23.clear()
        self.lineEdit_24.clear()
        self.lineEdit_25.clear()
        self.lineEdit_39.clear()

    # Add New Branch to System.
    def Add_Branch(self):
        
        # __init__
        canRun = True


        # Get data.
        branchData = self.getBranchDataFields()

        # Check and Kick.
        if branchData==False:
            canRun=False
        
        # Run.
        if canRun==True:
            # Save in Database.
            database.insertManyData("insert into branch values(?,?,?,?,?)",[branchData])

            # Save Action in History.
            action = {'action':'add new branch', 'extra':branchData[1], 'branch id':branch_id, 'employee id':employee_id}
            Tools.SaveActionToHistory(action)

            # Clean.
            self.clearBranchDataFields()


            # Notifications
            print("Branch Added !")

    """===== Category ====="""
    # Add new Categoey to the System.
    def Add_Category(self):

        #__inti__
        canRun = True

        # Get Data About Category
        id = database.generateID("select * from category")
        categoryName = self.lineEdit_30.text()
        
        # Check and Kick.
        if len( categoryName )==empty:
            canRun=False
            print("Please enter a category name.")

        # Run.
        if canRun==True:

            #Add Data To Database
            database.insertManyData("insert into category values(?,?,?)",[(
                id, categoryName, "None"
            )])

            # Cleart Fields
            self.lineEdit_30.clear()

            # Refreash Data in Combo Box
            self.Show_All_Categories()


            # Add this Aciotn in History
            action = {'action':'add new cateogry', 'extra':categoryName, 'branch id':branch_id, 'employee id':employee_id}
            Tools.SaveActionToHistory(action)
        
            # Notifications
            print("Category {} Added !".format(categoryName))

    """===== Publisher ====="""
    # Get Publisher Data Fields.
    def getPublisherDataFields(self):# Tool
        # Get Data About Publisher
        id = database.generateID("select * from publisher")
        publisherName = self.lineEdit_27.text()
        publisherLocation = self.lineEdit_26.text()

        # Check.
        fields = {'publisher name':publisherName, 'publisher location':publisherLocation}
        checkResult = Tools.checkFields(fields)

        # Output.
        if checkResult==True:
            return (id, publisherName, publisherLocation)
        else:
            return checkResult

    # Clear publisher Fields.
    def clearPublisherDataFields(self):
         # Cleart Fields
        self.lineEdit_27.clear()
        self.lineEdit_26.clear()

    # Add new Publisher to The System.
    def Add_Publisher(self):

        # __init__
        canRun = True

        # Get Data Fields.
        publisherData = self.getPublisherDataFields()

        # Check.      
        if publisherData==False:
            canRun=False

        # Run.
        if canRun==True:

            # Add Data To Database
            database.insertManyData("insert into publisher values(?,?,?)",[publisherData])
        
            # Clean.
            self.clearPublisherDataFields()

            # Save Action in History.
            action = {'action':'add new publisher', 'extra':publisherData[1], 'branch id':branch_id, 'employee id':employee_id}
            Tools.SaveActionToHistory(action)

            # Refreash System.
            self.Show_All_Publishers()

            # Notifications
            print("Publisher {} Added !".format(publisherData[1]))

    """===== Author ====="""
    # Add new Author to The System.
    def Add_Author(self):
        # Variables.
        authorName = self.lineEdit_29
        authorLocation = self.lineEdit_28

        # Run.
        thisObjects = {'name':authorName, 'location':authorLocation, 'branch':branch_id, 'employee':employee_id}
        authorName = TabWidget.SettingTab().fetchAuthorData(thisObjects)

        # Notifications
        if authorName != None:
            print("Author {} Added !".format(authorName))
            self.Show_All_Authors()


    """===== Employee ====="""
    # Add a New Employee & save changes in database.
    def Add_Employee(self):
        
        # Variables.
        employeeName = self.lineEdit_31
        employeeMail = self.lineEdit_32

        employeePhone = self.lineEdit_33
        employeeNationalID = self.lineEdit_34

        employeePeriority = self.lineEdit_35
        branch = self.lineEdit_53

        employeePassword = self.lineEdit_36
        employeeRepassword = self.lineEdit_37
        

        # Objects.    
        thisObjects = {
            'name':employeeName,
            'mail':employeeMail,
            'phone':employeePhone,
            'id':employeeNationalID,
            'periority':employeePeriority,
            'branch':branch,
            'password':employeePassword,
            'repassword':employeeRepassword,
            'current branch':branch_id,
            'current employee':employee_id
        }
        
        # Run.
        employee = TabWidget.SettingTab().fetchEmployeeData(thisObjects)

        if employee != None:
            # Notification
            print("Employee {} Added!".format(employee))
            
    # Chech the password and username from gui and connect with database
    def Check_Employee_toEdit(self): # Tool.
        # Variables & Objects.
        employeeName = self.lineEdit_43.text()
        employeePassword = self.lineEdit_44.text()

        thisObjects = {'name':employeeName, 'password':employeePassword}

        # Run.
        checkResult = TabWidget.SettingTab().checkEmployeeInSystem(thisObjects)

        if checkResult==True:
            # Enable Edit.
            self.groupBox.setEnabled(True)

            # Load Data.
            self.Edit_Employee_Data()
            
    # Show Employee data in fields to edit it
    def Edit_Employee_Data(self): # Tool.

    
        # Objects.   
        employeeName = self.lineEdit_43.text()
        employeePassword = self.lineEdit_44.text()
            
        emplpoyeePhone = self.lineEdit_40
        emplpoyeeMail = self.lineEdit_61

        emplpoyeeID = self.lineEdit_41
        emplpoyeePeriority = self.lineEdit_38
        emplpoyeeBranch = self.lineEdit_52

        emplpoyeeRepassword = self.lineEdit_42

        thisObjects = {
            'name':employeeName,
            'password':employeePassword,
            'phone':emplpoyeePhone,
            'mail':emplpoyeeMail,
            'id':emplpoyeeID,
            'periority':emplpoyeePeriority,
            'branch':emplpoyeeBranch,
            'repassword':emplpoyeeRepassword
        }


        # Run.
        TabWidget.SettingTab().loadEmployeeDataFields(thisObjects)


    # Save the Edits to database    
    def CommitEmployeeEdit(self):# Tool.
       # Objects.   
        employeeName = self.lineEdit_43
        employeePassword = self.lineEdit_44
            
        emplpoyeePhone = self.lineEdit_40
        emplpoyeeMail = self.lineEdit_61

        emplpoyeeID = self.lineEdit_41
        emplpoyeePeriority = self.lineEdit_38
        emplpoyeeBranch = self.lineEdit_52

        emplpoyeeRepassword = self.lineEdit_42

        thisObjects = {
            'name':employeeName,
            'password':employeePassword,
            'phone':emplpoyeePhone,
            'mail':emplpoyeeMail,
            'id':emplpoyeeID,
            'periority':emplpoyeePeriority,
            'branch':emplpoyeeBranch,
            'repassword':emplpoyeeRepassword,
            'current branch':branch_id,
            'current employee':employee_id
        }


        # Run.
        editEmployee = TabWidget.SettingTab().saveEmployeeDataChanges(thisObjects)
        
        # Output.
        if editEmployee != None:
            print("Employee {} Updated".format(employeeName))


    
    # Show Employeies in Combo Bos in System.
    def Show_Employee(self): # Tool.
        # Clear ComboBox
        self.comboBox_29.clear()
        self.comboBox_selectEmployee_forgetPassword.clear()


        # Get data from database
        employeis = database.getAll("select name from employee") 

        # Insert data in ComboBox
        for employee in employeis:
            self.comboBox_29.addItem(employee[0])
            self.comboBox_selectEmployee_forgetPassword.addItem(employee[0])



    # Check the employee permission and check it in GUI
    def Check_empployee_Permissions(self):

        # Variables.
        allBookCB = self.checkBox_30    ; allClientCB = self.checkBox_31
        addBookCB = self.checkBox       ; addClientCB = self.checkBox_4
        editBookCB = self.checkBox_2    ; editClientCB = self.checkBox_5
        delBookCB = self.checkBox_3     ; delClientCB = self.checkBox_6
        exportBookCB = self.checkBox_26 ; exportClientCB = self.checkBox_28
        importBookCB = self.checkBox_27 ; importClientCB = self.checkBox_29
        
        allPublicCB = self.checkBox_32
        bookTabCB = self.checkBox_7
        clientTabCB = self.checkBox_8
        dashbourdTabCB = self.checkBox_9
        historyTabCB = self.checkBox_10
        reportsTabCB = self.checkBox_11
        settingTabCB = self.checkBox_12

        allSettingCB = self.checkBox_33
        addDataCB = self.checkBox_21
        addEmployeeCB = self.checkBox_22
        editEmployeeCB = self.checkBox_24


        # Sort Data.
        employeeName = self.comboBox_29.currentText()
        admin = self.checkBox_25
        thisObjects = {
            'name':employeeName,
            'all book':allBookCB,
            'add book':addBookCB, 
            'edit book':editBookCB, 
            'delete book':delBookCB, 
            'export book':exportBookCB, 
            'import book':importBookCB,
            'all client':allClientCB,
            'add client':addClientCB,
            'edit client':editClientCB,
            'delete client':delClientCB,
            'export client':exportClientCB,
            'import client':importClientCB,
            'all public':allPublicCB, 
            'book':bookTabCB, 
            'client':clientTabCB, 
            'dashbourd':dashbourdTabCB, 
            'history':historyTabCB,
            'reports':reportsTabCB,
            'setting':settingTabCB,
            'all setting':allSettingCB,
            'add data':addDataCB,
            'add employee':addEmployeeCB,
            'edit employee':editEmployeeCB,
            'admin':admin,
        }

        # Run.
        TabWidget.SettingTab().loadEmployeePermissions(thisObjects)


        
    

    # Add a permossion to employee and save data in database
    def Edit_Employee_Permissions(self):

        # Variables.
        allBookCB = self.checkBox_30    ; allClientCB = self.checkBox_31
        addBookCB = self.checkBox       ; addClientCB = self.checkBox_4
        editBookCB = self.checkBox_2    ; editClientCB = self.checkBox_5
        delBookCB = self.checkBox_3     ; delClientCB = self.checkBox_6
        exportBookCB = self.checkBox_26 ; exportClientCB = self.checkBox_28
        importBookCB = self.checkBox_27 ; importClientCB = self.checkBox_29
        
        allPublicCB = self.checkBox_32
        bookTabCB = self.checkBox_7
        clientTabCB = self.checkBox_8
        dashbourdTabCB = self.checkBox_9
        historyTabCB = self.checkBox_10
        reportsTabCB = self.checkBox_11
        settingTabCB = self.checkBox_12

        allSettingCB = self.checkBox_33
        addDataCB = self.checkBox_21
        addEmployeeCB = self.checkBox_22
        editEmployeeCB = self.checkBox_24


        # Sort Data.
        employeeName = self.comboBox_29.currentText()
        admin = self.checkBox_25
        thisObjects = {
            'admin':admin, 'name':employeeName,
            'all book':allBookCB, 'all client':allClientCB,
            'add book':addBookCB, 'add client':addClientCB,
            'edit book':editBookCB, 'edit client':editClientCB,
            'delete book':delBookCB, 'delete client':delClientCB,
            'export book':exportBookCB, 'export client':exportClientCB,
            'import book':importBookCB, 'import client':importClientCB,
            'all public':allPublicCB, 'all setting':allSettingCB,
            'book':bookTabCB, 'add data':addDataCB,
            'client':clientTabCB, 'add employee':addEmployeeCB,
            'dashbourd':dashbourdTabCB, 'edit employee':editEmployeeCB,
            'history':historyTabCB,
            'reports':reportsTabCB,
            'setting':settingTabCB
        }

        # Run.
        employeePermissions = TabWidget.SettingTab().commitEmployeePermissions(thisObjects)

        if employeePermissions != None:
            print("Employee {} Updated Successfuly!".format(employeeName))

        
    # Make Reports about System for The Admin.
    def Admin_Report(self):
        
        # Report as Excel Files.
        self.ExportReportOfBooks()
        self.ExportReportAboutClients()
        self.ExportReportAboutEmployeies()


        # Notification.
        print("Files Exported!!")

    """=====================================================================================
    ================================= Profile Tab Functions ============================="""
    # Load profile information to the system.
    def LoadProfile(self):

        # Variables.
        name = self.label_105
        email = self.label_106
        joinDate = self.label_107
        image = self.label_104

        totalWorks = self.label_114

        myObjects = [ name, email, joinDate, totalWorks, image ]


        # Run.
        profileData = TabWidget.ProfileTab().getProfileData(employee_id)

        # Load Data.
        indx=0
        for label in myObjects:
            if label != image:
                label.setText( profileData[indx] )
                indx+=1
            else:
                self.pixmap = QPixmap( profileData[indx] )
                
                label.setPixmap(self.pixmap)

            

    # Logout user from the system.
    def LogoutSystem(self): # Tool.
        
        qApp.quit()
    
    # Load Navbar title data.
    def LoadNavbarData(self): # Tool.
        # Variables.
        currentTime = DateFile.dmyDate
        username = employee_id

        self.label.setText(currentTime)
        self.label_22.setText(username)
        
    """=====================================================================================
    ================================= Open Tabs Functions. =============================="""
    

    def Open_Login_Tap(self):
        self.tabWidget.setCurrentIndex(0)
        
    
    def Open_Reset_Password_Tap(self):
        self.tabWidget.setCurrentIndex(1)

    def OpenProfileTab(self):
        self.tabWidget.setCurrentIndex(9)

        self.LoadProfile()

    def Open_Daily_Movment_Tap(self):
        self.tabWidget.setCurrentIndex(2)
        self.TaodayWidget.setCurrentIndex(0)

        # Refresh Data
        self.LoadNavbarData()
        tableName = self.tableWidget_2
        hpTool.showDailyBooks({'table':tableName})

        
        
        
    def Open_Books_Tap(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(0)
        self.Show_All_Books()

        # Set defaut image
        self.pixmap = QPixmap(default_book_image)

        # Add Image to Label
        self.label_19.setPixmap(self.pixmap)

        # Notification
        self.statusBar().showMessage("Books Loaded to Screen !!")


    
    def Open_Clients_Tap(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)
        
        # Load data to screen
        self.Show_All_Clients()

        # Notification
        self.statusBar().showMessage("Clients Loaded to Screen !!")


    
    def Open_Dashboard_Tap(self):
        self.tabWidget.setCurrentIndex(5)
        
        self.LoadSystemInformation()

    def Open_History_Tap(self):
        self.Show_History()
        self.tabWidget.setCurrentIndex(6)

    def Open_Reports_Tap(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_5.setCurrentIndex(0)

        # Refresh data
        self.Show_All_Book_Reports()
        self.Show_All_Client_Reports()
        self.Show_Employee_Report()       



    def Open_Settings_Tap(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(0)

        # Refresh data.
        self.Show_Employee()




        






def Show_Login():

    app = QApplication(sys.argv)
    window = login_frame.Login()
    window.show()
    app.exec_()


    
 


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    Show_Login()
    
    if login_frame.loginStatus == True and login_frame.resetPasswordStatus==False :
        main()

    elif login_frame.resetPasswordStatus==True :
        main()
