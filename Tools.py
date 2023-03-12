from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Database, DateFile, random

# GLobal Variable
empty = 0
db = Database.ConnectSqlite3()


# Check Fields Passed.
def checkFields(fields): # --> Tool to Check.
    """Check the fields passed.\n
    fields --> pass the fields in dictionary as {FieldName : FieldDataObject}.\n
    for Ex --> 'search text':lineEdit.text"""

    fieldsStatus = True
    
    # WORK
    for field in fields:
        if len( fields[field] ) == empty:
            print("Please {} cannot be empty.".format(field) )
            fieldsStatus = False
            break

    # OUTPUT
    return fieldsStatus

# Show data in table widget.
def insertNewRow(tableName, row): # --> Tool to do in UI.
    """Tool to insert a new row in the table widget.\n
    tableName --> pass the object name\n
    row --> pass the current row in showDataInTable() when it work."""
    
    # Insert new Row
    rowsLength = tableName.rowCount()
    if rowsLength <= row:
        tableName.insertRow(rowsLength)

# Edit table widget function
def editTableWidgetItem(a):
    print(a)
    print("Edit Table Widget Item")

# Delete table widget function
def delTableWidgetItem():
    print("Delete Table Widget Item")


# Insert QDialogButtonBox in TableWidget.
def insertQDialogButtonBoxInTable(tableName, btns, column):# Tool.
    """tableName --> pass the object like self.tableWidget\n
    btns --> tuple data type pass the button's functions in order\n
    ( Edit function, delete function)\n
    column --> pass intger for the action column."""

    # Variables.
    tableLength = tableName.rowCount()
    EditFunction = btns[0]
    DeleteFunction = btns[1]

    # Loop through table.
    for row in range(tableLength):
        # Set DialogButtonBox. 
        btn = QDialogButtonBox(tableName)
        btn.setStyleSheet("width:200px; font-size:10pt;")

        # Add Button.
        btn.addButton('Edit',btn.AcceptRole)
        btn.addButton('Del',btn.HelpRole)

        btn.accepted.connect(EditFunction)
        btn.helpRequested.connect(DeleteFunction)
        
        tableName.setCellWidget(row, column, btn)


# Normal Function.
def showDataInTable(tableName, tableData): # Work with GUI --> Show in table widget.
    """ tableName --> pass the object name\n
    tableData --> pass the data to show it in the table."""

    # Insert data into table
    for row , form in enumerate(tableData):
        
        # INSERT ROW
        insertNewRow(tableName, row)

        # Full Column
        for col, item in enumerate(form):
            
            tableName.setItem(row, col, QTableWidgetItem(str(item)) )
            col+=1 # to new column

# Cutomize Function.
def showBooksInTable(tableName, tableData): # Work with GUI --> Show in table widget.
    """This is a Customize function to insert books in table in client report tab.\n 
    tableName --> pass the object name\n
    tableData --> pass the data to show it in the table."""

    # Variables.
    dataLength = len(tableData)

    # Insert data into table
    for row in range(dataLength):
        
        # INSERT ROW
        insertNewRow(tableName, row)

        # Full Column
        tableName.setItem(row, 4, QTableWidgetItem(str(tableData[row])) )

# Get client name from id
def getClientName(clientId) : # --> Tool to Get. 
        """Search about a client with his National ID."""
        thisName = db.getOne("select name from clients where national_id = {}".format(int(clientId)))
        if len( thisName ) == 0 :
            return None
        else:
            return thisName[0]


# Isert an action to History atble
def SaveActionToHistory(objects):
    """insert action that happedn to the history table in database.\n
    objects needed --> action, extra, branch id, employee id"""

    # VARIABLES
    historyID = db.generateID("select * from history")
    employee = objects['employee id']
    branch = objects['branch id']
    action = objects['action']
    extra = objects['extra']
    currentDate = DateFile.dmDate

    # SORT DATA
    thisData = [(historyID, employee, action, currentDate, branch, extra)]
    
    # LOAD
    db.insertManyData("insert into history values(?,?,?,?,?,?)",thisData)
    

# Calculator for Rent or Retrieve.
def CalulatRent(bookName):
    """minus from quantity."""

    # Variables.
    quantity = db.getOne("select quantity from books where title like '%{}%'".format(bookName))[0]
    newQuantity = quantity-1

    if newQuantity < 0:
        newQuantity = 0

    # Update.
    db.updateData("update books set quantity = {} where title like '%{}%'".format(newQuantity, bookName))

    return newQuantity


def CalulatRetrieve(bookName):
    """plus to quantity."""

    # Variables.
    quantity = db.getOne("select quantity from books where title like '%{}%'".format(bookName))[0]
    newQuantity = quantity+1

    # Update.
    db.updateData("update books set quantity = {} where title like '%{}%'".format(newQuantity, bookName))


# Get all Client's Books.
def getClientBooks(Clients):
    """Looping in clients then calculate all books the client has rent it."""
    # Variables.
    clientBooks = []

    # get client's book
    for client in Clients:
        
        calculateBooks = db.getAll("select book_id from daily_movments where client_id = {}".format(client[0]))
        clientBooks.append( len(calculateBooks) )

    return clientBooks

# Get Employee Name.
def getEmployeeName(employeies):
    """Loopping through employeies to get them Names.\n
    return a list of employeies names"""

    # Variables.
    employeiesNames = []

    # Loop.
    for employee in employeies:
        employeeName = db.getOne("select name from employee where name = '{}'".format(employee[0]))
        
        if len(employeeName)==empty and "admin" not in employeiesNames:
            employeiesNames.append("admin")
        
        elif employeeName not in employeiesNames and len(employeeName)!=empty:
            employeiesNames.append(employeeName)

    
    # Output.
    return employeiesNames

# Show employee Title in the Table --> Customize Function.
def showEmployeeTitleInTable(tableName, employeeName):
    """Customize function to insert a new row with employee data Title.\n
    in table widget at employee report tab.\n
    pass tablewidget object --> tableName.\n
    employeeID --> an Employee ID."""

    
    # Variables.
    row = tableName.rowCount()
    employeeData = db.getOne("select name, national_id, Branch from employee where name = '{}'".format(employeeName))
   
    # Indexies.
    nameInx=0; idIndx=1; branchIndx=2;


    # INSERT ROW
    insertNewRow(tableName, row)
    
    if employeeName=="admin":

        # Full Column
        tableName.setItem(row, 0, QTableWidgetItem("admin") )
        tableName.setItem(row, 1, QTableWidgetItem("admin") )
        tableName.setItem(row, 2, QTableWidgetItem("-----") )
        tableName.setItem(row, 3, QTableWidgetItem("-----") )
        tableName.setItem(row, 4, QTableWidgetItem("admin") )

    elif employeeData != empty:
        # Full Column
        tableName.setItem(row, 0, QTableWidgetItem( str(employeeData[nameInx]) ) )
        tableName.setItem(row, 1, QTableWidgetItem( str(employeeData[idIndx]) ) )
        tableName.setItem(row, 2, QTableWidgetItem("-----") )
        tableName.setItem(row, 3, QTableWidgetItem("-----") )
        tableName.setItem(row, 4, QTableWidgetItem( str(employeeData[branchIndx]) ) )

# Get Employee Data to Show it in The Table --> Tool for showEmployeeDataInTable().
def getEmployeeData(tableName, employeeName):
    """employeeName --> The Employee Name."""

    # Get Data.
    employeeData = db.getAll("select employee, actions, date from history where employee = '{0}' or employee = '0'".format(employeeName))
    
    # Insert data into table
    for row , form in enumerate(employeeData):
        
        # INSERT ROW
        insertNewRow(tableName, row)

        # Sort Data.
        name = form[0]
        action = form[1]
        date = form[2]


        # Check.
        if name=='0':
            # Full Column
            tableName.setItem(row, 0, QTableWidgetItem( str("admin") ) )
        else:
            tableName.setItem(row, 0, QTableWidgetItem( str(name) ) )

        tableName.setItem(row, 2, QTableWidgetItem( str(action) ) )
        tableName.setItem(row, 3, QTableWidgetItem( str(date) ) )

    

# Show the Employee data in the Table Widget --> Customize Function.
global employeiesName
employeiesName = []
def showEmployeeDataInTable(tableName, employeeName):
    """tableName --> tableWidget object.\n
    employeeName --> The Employee Name."""  

    # Variables.
    global employeiesName

    # Insert Title.
    if employeeName not in employeiesName:
        showEmployeeTitleInTable(tableName, employeeName)

    # Insert Others Data.
    getEmployeeData(tableName, employeeName)

    # Save Employee.
    employeiesName.append(employeeName)


# Convert Image to Binary Data
def convertToBinaryData(filename):

    # Convert binary format to images or files data
    with open(filename, 'rb') as file:
        blobData = file.read()
    
    # Return a Binary Data
    return blobData


# Get Employee report tableWidget Data.
def getEmployeeTableWidgetData(table):
    """Get the data from tableWidget in employee report tab.\b
    table --> tableWidget object."""

    # Variables.
    rows = table.rowCount()
    tableData = []

        
    for row in range(rows):
        
        # Looppint through columns.
        data = []
        for col in range(5):
            # Current Row Data.
            thisData = table.item(row, col)

            if thisData==None:
                data.append("    ")
            else:
                data.append(thisData.data(0))

        # Insert Data to the List.
        tableData.append(data)

    # Output.
    return tableData

# Open a Dialog Window and choose Picture.
def getImage(pixmap, label):
       
    # Open Dialog and Get Picture
    imgName = QFileDialog.getOpenFileName("Get the Image", "/home/izy/Desktop/Library System", "All Files (*);;PNG Files (*.png)")

    # Open The Image this run
    print(imgName)

    pixmap = QPixmap(imgName[0])

    # Add Image to Label
    label.setPixmap(pixmap)

# Generate new password --> Tool.
def generateNewPassword():
    "Randomly integer password."
    return random.randint(11111,99999)


# Get the New Password For Employee.
def getNewPassword(employee):
    """check employee name in database"""

    # Variables.
    newPassword = 0

    # Check Employee    
    isEmployeeExit = db.getOne("select name from employee where name = '{}'".format(employee))

    if len(isEmployeeExit)==empty:
        return newPassword  
    
    else:
        newPassword = generateNewPassword()
        return newPassword


        