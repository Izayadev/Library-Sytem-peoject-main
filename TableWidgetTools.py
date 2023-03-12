#QTableWidget Tools File
from Tools import *
import TabWidget

     
# ButtonsFunctions Class to Work with Any Button's Function in the Table Widget.
class ButtonsFunctions():

    # button for order a book.
    def OrderBook(self):

        # Open.
        tab.setCurrentIndex(2)

        # Get Book Title from Table Widget.
        row = table.currentRow()
        bookTitle = table.item( row, 0).data(0)
        
        # Set Book Name.
        label.setText(bookTitle)

        # Set the price.
        priceValue = str( TabWidget.DailyMovment().getBookPrice(bookTitle) )
        price.setText( "The Price: "+priceValue+"$"+"\nNote: Rent fee: 2$" )

        print("You Ordered Book That name is {}".format(bookTitle))


    # button for open edit tab for books's tab.
    def EditTab(self):

        # Open.
        tab = myOptions['tab']
        tab.setCurrentIndex(2)

        # Get Book Code from Table Widget.
        row = clickTable.currentRow()
        bookCode = clickTable.item( row, 0).data(0)

        # Set Book Code in Line Edit.
        code = myOptions['text'].setText(bookCode)  

        # Run Script to Load Data in Fields.
          


"""=========================================================================================
============================== ButtonsFunctions Class's Methuds ========================="""
# Order a Book.
def OrderBookMethud():

    ButtonsFunctions().OrderBook()

# Open Edit tab Function
def OpenEditTab():
    ButtonsFunctions().EditTab()

# Delete row's data Function
def DeleteRowsData():
    print("Deleted")


# Clicks Class to wotk with clicks in the table widget.
class Click():

    def DoubleClick(self, tableName, function, options):
        """tableName --> tableWidget\n
        function --> function that do something\n
        options --> {'tab':tabWidget, 'text':lineEdit}"""

        # Variables.
        global myOptions, clickTable
        clickTable = tableName
        myOptions = options

        # Do this.
        tableName.cellDoubleClicked.connect(function)

# Buttons Class to work with any button in the table widget.
class Buttons():

    # Insert Button into Table.
    def insertDialogButton(self, tableName, functions, row, column): # Tool.
        """inset two button edit and delete\n
        functions --> tuple of two functions ( EditFunction, DeleteFunction)"""


        # Set DialogButtonBox. 
        btn = QDialogButtonBox(tableName)
        btn.setStyleSheet("width:200px; font-size:10pt;")

        # Add Button.
        btn.addButton('Edit',btn.AcceptRole)
        btn.addButton('Del',btn.HelpRole)

        btn.accepted.connect( functions[0] ) #EditFunction
        btn.helpRequested.connect( functions[1] ) #DeleteFunction
        
        tableName.setCellWidget(row, column, btn)

    # Insert QDialogButtonBox in TableWidget.
    def insertQDialogButtonBoxInTable(self, tableName, btn, column):# Tool.
        """tableName --> pass the object like self.tableWidget\n
        btns --> tuple data type pass the button's functions in order\n
        ( Edit function, delete function, tabWidget)\n
        column --> pass intger for the action column."""

        # Variables.
        global tableDialog, tabDialog
        tableDialog = tableName
        tabDialog = btn[2]
        

        tableLength = tableName.rowCount()

        # Loop through table.
        for row in range(tableLength):
            # Initialize Buttons.
            button = QPushButton(tableName)
            button2 = QPushButton(tableName)

            button.setText('edit')
            button2.setText('del')

            
            # Set Function.        
            button.clicked.connect(btn[0])
            button2.clicked.connect(btn[1])


            # Insert Button.
            layout = QHBoxLayout(tableName)
            layout.addWidget(button)
            layout.addWidget(button2)

            box = QWidget()
            box.setLayout(layout)

            
            tableName.setCellWidget(row, column, button)
            
            # # Insert Buttons.
            # functions = ( btn[0], btn[1] )
            # self.insertDialogButton(tableName, functions, row, column)
        
    # Insert QPushButton into TableWidget.
    def insertQPushButtonIntoTable(self, tableName, btn, column):
        """tableName --> pass the table object\n
        btn --> pass button's properties like\n
        { 'text':'button name', 'do':function, 'label':lineEdit, 'tab':TabWidget, 'price':label }\n
        column --> pass intger about where btn will be."""

        # Variables.
        global label, tab, price, table
        table = tableName
        label = btn['label']
        price = btn['price']
        tab = btn['tab']

        tableLength = tableName.rowCount()
        
        
        function = btn['do']
        text = btn['text']

        # Loop through table.
        for row in range(tableLength):
            
            # Initialize Buttons.
            button = QPushButton(tableName)
            button.setText(text)

            
            # Set Function.        
            button.clicked.connect(function)


            # Insert Button.
            tableName.setCellWidget(row, column, button)

            

