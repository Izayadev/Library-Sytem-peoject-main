from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Database
# GLobal Variable
empty = 0
db = Database.ConnectSqlite3()


# Check Fields Passed.
def checkFields(fields): # --> Tool to Check.
    """Check the fields passed.\n
    fields --> pass the fields in dictionary as {FieldName : FieldData}."""

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
    row --> pass the current row in showBooksInTable() when it work."""
    
    # Insert new Row
    rowsLength = tableName.rowCount()
    if rowsLength <= row:
        tableName.insertRow(rowsLength)

def showBooksInTable(tableName, tableData): # Work with GUI --> Show in table widget.
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

# Get client name from id
def getClientName(clientId) : # --> Tool to Get. 
        """Search about a client with his National ID."""
        thisName = db.getOne("select name from clients where id = {}".format(clientId))
        return thisName

# Convert Image to Binary Data
def convertToBinaryData(filename):

    # Convert binary format to images or files data
    with open(filename, 'rb') as file:
        blobData = file.read()
    
    # Return a Binary Data
    return blobData



