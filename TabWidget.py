from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Tools as tool
import Database, DateFile, TableWidgetTools



# Globla Variables

db = Database.ConnectSqlite3()
empty = 0
adminAccess = 0
reusedData = ()

class DailyMovment():
    
    # Show Daily Books
    def showDailyBooks(self, dailyObjects): # Work with DB --> DailyMovments Table.
        """get the books from database dn load it in the table in the daily movments tab.\n
        dailyObject --> pass a data as dictionary.\n
        data are --> table"""

        # VARIABLES
        table = dailyObjects['table']
        # GET 
        dailyBooks = db.getAll("select book_id, client_id, type, book_from, book_to from daily_movments")

        # CHECK
        if len( dailyBooks ) != empty:
            # CHECK
            tool.showDataInTable(table, dailyBooks)    
        
        else:
            print("No Books!")

    # Search in daily movment tab
    def getDailyBooksSearch(self,dsObjects) :# Work with DB --> DailyMovment Table.
        """search about a book in daily movment table [tab].\n
        dsObjects (daily search objects) -- > pass as dectionary.\n
        objects are --> search text, table"""

        # VARIABLES
        searchText = dsObjects['search text']
        table = dsObjects['table']

        # SEARCH
        booksFounded = db.getAll("select book_id, type, client_id, Book_from, Book_to from daily_movments where book_id like '%{}%'".format(searchText))

        # NOTIFICATIONS
        print("Searching in Last Daily Movments...")
        print("There are {} books founded".format( len(booksFounded) ))

        # REFRESH
        if len( booksFounded ) != empty:
            
            table.clear()
            tool.showDataInTable(table, booksFounded)
        else:
            print("No Books")



    # Search in order a book tab --> Workable
    def getOrderTabSearch(self,tabObjects): # Work with DB --> books table.
        """Search about a book and use the result as a data to show it in the table.\n
        tabObject --> pass the objects as a dictionary."""
        # GET
        searchText = tabObjects['search text'].text()
        label = tabObjects['label']
        price = tabObjects['price']
        tab = tabObjects['tab']
        
        # CHECK
        checkResult = tool.checkFields( {'search text':searchText} )

        if checkResult != empty:

            # SEARCH
            booksFounded = db.getAll("select title, author_id, part_order, price, quantity from books where title like '%{0}%' or code like '%{0}%'".format(searchText))

            # NOTIFICATIONS
            print("Searching in books...")
            print("There is {} Books founded ".format(len(booksFounded)))

            # REFRESH
            if len( booksFounded ) != empty:
                # Insert Data.
                tool.showDataInTable(tabObjects['table'], booksFounded)

                # Insert Buttons.
                btn = {'text':'Order', 'do':TableWidgetTools.OrderBookMethud, 'label':label, 'tab':tab, 'price':price }
                TableWidgetTools.Buttons().insertQPushButtonIntoTable(tabObjects['table'],btn, 5)
                
            else:
                print("No Books")
        

            # OUTPUT
            return booksFounded


    # get book price.
    def getBookPrice(self,bookName): # Tool.
        """get Book nae then check its price and return it."""

        # Check.
        price = db.getOne("select price from books where title = '{}'".format(bookName))

        if len(price) == empty:
            print("There is no book with this name {}".format(bookName))
            return 0
        else:
            return price[0]



    # Get Order Derails
    def getOrderDetails(self,orderObjects): # Work with DB --> Books table.
        """get the data from fields, work in ,check it, then submit it into database.\n
        orderObjects --> tabObject --> pass the objects as a dictionary.\n
        objects are --> empoyee id, branch id, book title, client id, price, order type, label.\n"""

        # __init__
        canRun = True
        thisMessage = ""


        # VARIABLES
        label = orderObjects['label']
        employeeID = orderObjects['employee id']
        branchID = orderObjects['branch id']

        bookTitle = orderObjects['book title']
        clientID = orderObjects['client id']

        clientName = tool.getClientName(clientID)
        price = self.getBookPrice(bookTitle)
        orderType = orderObjects['order type'].currentText()
        

        currentDate = DateFile.dmyDate # the date
        retrieveData = "NONE"


        # Check and Kick.
        if clientName==None:
            canRun=False
            thisMessage = "Wrong the client id {} is wrong".format(clientID)
            



        """=== PROSSES ==="""
        # MESSAGE
        if orderType == 'Rent' and canRun:
            # Minus Quantity
            quantity = tool.CalulatRent(bookTitle)
            
            if quantity > 0 :
                price = 2 # Rent Price
                retrieveData = DateFile.afterDays(7)
                thisMessage = """Dear {}\n
                You Have Ordered the book {},\n
                and you may return it in one week from this date {} .""".format(clientName, bookTitle, retrieveData)
            else:
                thisMessage = "We dont have any more of this book."
                canRun = False

        elif orderType == 'Retrieve' and canRun:
            # Plus Quantity.
            print("here")
            tool.CalulatRetrieve(bookTitle)

            thisMessage = """Dear {}\n
            We Retrieve this book {} from you,\n
            Thank you for visit us  .""".format(clientName, bookTitle)
        
        elif orderType == 'Buy' and canRun:
            # Minus Quantity
            quantity = tool.CalulatRent(bookTitle)

            if quantity > 0 :
                retrieveData = "Not Needed"
                thisMessage = """Dear {}\n
                You Have Bought the book {} ,\n
                Thank for Visit Us .""".format(clientName, bookTitle)
            else:
                thisMessage="We dont have any more of this book."
                canRun = False

            
        # NOTIFICATION
        label.setText(thisMessage)

        # Run and Save data in Database.
        if canRun==True:
            # SUBMIT
            dailyMpvmentsID = db.generateID("select * from daily_movments")
            thisData = [(
                dailyMpvmentsID, bookTitle, clientID, orderType, price,
                currentDate, branchID, currentDate, retrieveData,
                employeeID 
            )]
            db.insertManyData("insert into daily_movments values(?,?,?,?,?,?,?,?,?,?)",thisData)

            historyID = db.generateID("select * from history")
            db.insertManyData("insert into history values(?,?,?,?,?,?)",[
                (historyID, employeeID,
                orderType+" a Book", currentDate,
                branchID, bookTitle)
            ])

        
class BookTab():

    # Get bookd from database and show in the table widget.
    def getAllBooks(self, thisObjects):
        """After get book, show it, return notification.\n
        thisObjects --> pass as dictionary.\n
        Objects are --> branch id, table, tab, text"""

        # VARIABLES
        branchAccess = thisObjects['branch id'] 
        table = thisObjects['table']
        tab = thisObjects['tab']
        lineText = thisObjects['text']

        

        # TABLE DATA
        if branchAccess == adminAccess:
            booksData = db.getAll("select code, title, category_id, author_id, price from books")

        else:
            booksData = db.getAll("select code, title, category_id, author_id, price from books where Branch = '{}'".format(branchAccess))


        # INSERT
        tool.showDataInTable(table, booksData)

        # Insert buttons in table.

        # btn = ( TableWidgetTools.OpenEditTab, TableWidgetTools.DeleteRowsData, tab)
        options = {'tab':tab, 'text':lineText}
        TableWidgetTools.Click().DoubleClick(table, TableWidgetTools.OpenEditTab, options)
        # TableWidgetTools.Buttons().insertQPushButtonIntoTable(table,{})
        # TableWidgetTools.Buttons().insertQDialogButtonBoxInTable(table, btn, 5)

        # NOTIFICATIONS
        print("Books loaded in the screen!")        


    # Search about a book via title, author.
    def searchAboutBook(self, thisObjects):
        """U can search via title, author and an other useful data.\n
        thisObjects --> pass data as dictionary.\n
        objects are --> search text, table, branch id"""

        # VARIABLES 
        branchAccess = thisObjects['branch id']
        searchText = thisObjects['search text']
        table = thisObjects['table']
        sqlQuery = """select code, title, category_id, author_id, price from books
        where title like '%{0}%' or category_id like '%{0}%' or author_id like '%{0}%' or description like '%{0}%'"""
        
        
        # GET
        if branchAccess == adminAccess:
            bookFounded = db.getAll( sqlQuery.format(searchText) )

        else:
            bookFounded = db.getAll( sqlQuery.format(searchText)+" and Branch = '{}'".format(branchAccess) )

        # NOTIFICATIONS
        print("There are {} books founded".format( len(bookFounded) ))


        
        # SHOW
        if len(bookFounded) == empty:
            print("No book founded!")
        else:
            table.clearContents()
            tool.showDataInTable(table, bookFounded)

    # Submit those data to add a new book.
    def submitNewBook(self, thisObjects):
        """Get book details, save it, load it, notification cutomers\n
        thisObjects are a dictioanry data type pass thoses data in order(11 elemnts)\n
        title, description, author, category, publisher, part, price, code, barcode, status, quantity, image, branch id, employee id
        """

        # VARIABLES
        bookTitle = thisObjects['title']
        bookDescription = thisObjects['description']
        bookAuthor = thisObjects['author']
        bookCategory = thisObjects['category']
        bookPublisher = thisObjects['publisher']
        bookPart = thisObjects['part']
        bookPrice = thisObjects['price']
        bookCode = thisObjects['code']
        bookbarcode = thisObjects['barcode']
        bookStatus = thisObjects['status']
        bookQuantity = thisObjects['quantity']
        bookImage = thisObjects['image']

        currentDate = DateFile.dmyDate

        bookID = db.generateID("select * from books")
        branchID = thisObjects['branch id']
        employeeID = thisObjects['employee id']

        # SAVE IN DATABASE        
        db.insertManyData("insert into books values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",[(
            bookID, bookTitle, bookDescription, bookCategory,
            bookCode, bookbarcode, bookPart,
            bookPrice, bookPublisher, bookAuthor,
            bookStatus, currentDate, bookQuantity, branchID, bookImage
        )])

        # SAVE ACTION
        if branchID==adminAccess or employeeID==adminAccess:
            thisData = {'action':"Add new Book", 'extra':bookTitle, 'branch id':"admin", 'employee id':"admin"}

        else:
            thisData = {'action':"Add new Book", 'extra':bookTitle, 'branch id':branchID, 'employee id':employeeID}
        
        tool.SaveActionToHistory(thisData)

        # NOTIFICATIONS
        print("The new book {} added".format(bookTitle) )

    # Submit those Edit book.
    def submitEditBook(self, thisObjects):
        """Load data in fields, handle changes, svae it.\n
        thisObjects is a dictionary data type take those arguments\n
        book code, branch id, book title, book part, book image,
        book quantity, book author, book description, book category, 
        book publisher, book price, book code, pixmap"""

        
        # VARIABLES
        bookSearch = thisObjects['book search']; branchID = thisObjects['branch id']
        bookCode = thisObjects['book code']; 
        bookTitle = thisObjects['book title']
        bookPart = thisObjects['book part']; bookImage = thisObjects['book image']
        bookQuantity = thisObjects['book quantity']; bookAuthor = thisObjects['book author']
        bookDescription = thisObjects['book description']; bookCategory = thisObjects['book category']
        bookPublisher = thisObjects['book publisher']; bookPrice = thisObjects['book price']
        pixmap = thisObjects['pixmap']; bookStatus = thisObjects['book status']

        # indexies
        title=1; desciption=2; category=3; 
        code=4; part=6; price=7; publisher=8; author=9 ;
        status=10; quantity=12; image = 14

        

        # GET 
        if branchID == adminAccess:
            sqlQuery = "select * from books where code like {}".format( bookSearch.text() )

        else:
            sqlQuery = "select * from books where code like {} and Branch = {}".format(bookSearch.text(), branchID)
        
        thisBookData = db.getOne(sqlQuery)

        # CHECK
        if len( thisBookData ) == empty:
            print("Wrong!!... There is no book has this {} code".format( bookSearch.text() ))

        elif len( thisBookData ) != empty:
            
            # Load data to fields
            bookTitle.setText(thisBookData[title])
            bookDescription.setPlainText(str(thisBookData[desciption]))

            bookCategory.setCurrentText(thisBookData[category])
            bookPrice.setText(str(thisBookData[price]))

            bookCode.setText(thisBookData[code])
            bookPublisher.setCurrentText(thisBookData[publisher])

            bookAuthor.setCurrentText(thisBookData[author])
            bookPart.setText(str(thisBookData[part]))

            bookQuantity.setText(str(thisBookData[quantity]))
            bookStatus.setCurrentText(thisBookData[status])

            codeID = bookSearch.text()
            # Get a binary image
            imageUrl = thisBookData[image]

            # Open The Image 
            pixmap = QPixmap(imageUrl)

            # Add Image to Label
            bookImage.setPixmap(pixmap)


            # NOTIFICATION
            print("{} Loaded to edit..".format( bookTitle.text() ))

            # RETURN to REUSE
            global reusedData
            reusedData = (
                bookTitle, bookDescription, bookCategory,
                bookCode, bookPart, bookPrice,
                bookPublisher, bookAuthor, bookStatus,
                bookQuantity, codeID
            )


            

    # Submit change to database
    def submitChange(self):
        """Variable reused declayering in submitEditBook Function and set to be global."""

        # INDEXIES
        title = 0; desciption = 1; category = 2;
        code = 3; part = 4; price = 5;
        publisher = 6; author = 7; status = 8;
        quantity = 9; code2 = 10;

        # UPDATE 
        updateSqlQuery = """update books
                set title = '{0}',
                description = '{1}',
                category_id = '{2}',
                code = '{3}',
                part_order = {4},
                price = '{5}',
                publisher_id = '{6}',
                author_id = '{7}',
                status = '{8}',
                quantity = {9}
                where code = {10}
                """.format(
                    reusedData[title].text(), reusedData[desciption].toPlainText(), reusedData[category].currentText(),
                    reusedData[code].text(), reusedData[part].text(), reusedData[price].text(),
                    reusedData[publisher].currentText(), reusedData[author].currentText(), reusedData[status].currentText(),
                    reusedData[quantity].text(), reusedData[code2]
                )
                
                
        db.updateData(updateSqlQuery)

        print("Hai done!")

    # Delete a Book from database and system.
    def submitDeleteBook(self, thisObjects):
        """Delete a bok with its Code number.\n
        thisObjects in order --> code, branch id, employee id"""

        # GET
        codeNumber = thisObjects['code']
        branch = thisObjects['branch id']
        employee = thisObjects['employee id']
        extra = "Book code"+str(codeNumber)

        db.deleteData("delete from books where code = {}".format(codeNumber))

        # SAVE ACTION
        if branch==adminAccess or employee==adminAccess:
            thisData = {'action':'Delete book','extra':extra, 'brcnh id':'admin', 'employee id':'admin'}
        else:
            thisData = {'action':'Delete book','extra':extra, 'brcnh id':branch, 'employee id':employee}
                
        tool.SaveActionToHistory({'action':'Delete book','extra':extra, 'brcnh id':branch, 'employee id':employee})

        # NOTIFICATION
        print("Book deleted !!")

class ClientTab():

    def addNewClient(self,objects):
        """Add new client to system save it loaded in screen.\n
        objects --> in order <name, mail, phone, id>"""

        # Variables
        clientName = objects['name'].text()
        clientMail = objects['mail'].text()
        clientPhone = objects['phone'].text()
        clientID = objects['id'].text()

        currenDate = DateFile.dmyDate
        dbID = db.generateID("select * from clients")

        # Check Data Fields.
        thisFields = {'client name':clientName,
                      'cleint mail':clientMail,
                      'client phone':clientPhone,
                      'client id':clientID}
        checkResult = tool.checkFields(thisFields)
        
        # Check and Run.
        if checkResult == True:
            # Add to database.
            thisData = [(
                dbID, clientName, clientMail, clientPhone, currenDate, clientID
            )]
            db.insertManyData("insert into clients values(?,?,?,?,?,?)",thisData)

            return 1
        else:
            return 0
        

    def getSearchData(self,objects):
        """get the search text, search with it then return data.\n
        objects you may need\n
        < search text,"""

        # Variables.
        searchText = objects['search text']
        tableName = objects['table']

        # Check search text then Run.
        if len(searchText) == empty:
            print("please enter search text first!!")
        else:

            # Search
            searchData = db.getAll("select name, mail, phone, national_id from clients where name like '%{0}%' or mail like '%{0}%' or phone like '%{0}%' or national_id like '%{0}%'".format(searchText))

            # Check and Print.
            if len( searchData ) == empty:
                print("There is no client founded in database.")
            else:
                print(searchData)

                # Show in table.
                tableName.clearContents()
                tool.showDataInTable(tableName, searchData)


    def loadCleintDataToEdit(self,text):
        """search about client in database then get his data and load it in fields to be editable."""

        # Variables.
        searchText = text


        # Search.
        clientData = db.getOne("select name, mail, phone, national_id from clients where name = '{0}' or mail = '{0}' or phone = '{0}' or national_id = '{0}'".format(searchText))

        if len( clientData ) == empty:
            print("We cannot find this client, please try again.")
            return ()
        else:
            return clientData


    def updateClientData(self, clientData):
        """Submit and update the data in database.\n
        clientData Keys in this order-->\n
        <id, name, mail, phone, national id>"""
        
        # Variables.
        id = clientData['id']
        clientName = clientData['name']
        clientMail = clientData['mail']
        clientPhone = clientData['phone']
        clientID = clientData['national id']
        
        # Run
        db.updateData("update clients set name = '{}', mail = '{}', phone = '{}', national_id = {} where id = {}".format(
            clientName, clientMail, clientPhone, clientID, id
        ))

        # Notification.
        print("Updated !!")


class HistoryTab():

    def getSearchAboutText(self, searchText, table):
        """Search in history by employee, branch, action, date or extra."""

        # __init__
        canRun = True
        
        # Get Search Data.
        history = db.getAll("select employee, actions, branch_id, date, extra from history where employee like '%{0}%' or branch_id like '%{0}%' or actions like '%{0}%' or date like '%{0}%' or extra like '%{0}%'".format(searchText))
    
        # Check and Kick.
        if len( history ) == empty:
            canRun = False
            print("There is no Data found like what you search!!")
     
        # Show in Table.
        if canRun:
            table.clearContents()
            tool.showDataInTable(table, history)


class ReportsTab():

    # Get Report of data about books and show it in the table.
    def getBookReport(self, tableName):
        """Get a list of books and show it in the table."""

        # Get Data.
        booksData = db.getAll("select code, title, category_id, author_id, Branch, quantity from books")

        # Show in Table.
        tool.showDataInTable(tableName, booksData)


    # Get a Report of Data about Clients and Show it in The Table.
    def getClientsReport(self, table):
        """Load Client Data in the Table in Client Report tab.\n
        table is --> table widget in gui."""
        
        # Get Clients Data.
        clientsData = db.getAll("select national_id, name, mail, phone from clients")

        # Variables.
        countingClientsBooks = tool.getClientBooks(clientsData)

        # Show in Table.
        tool.showDataInTable(table, clientsData)
        tool.showBooksInTable(table, countingClientsBooks)

        
    # Get a Report of Data about Employeies and Show it in The Table.
    def getEmployeiesReport(self, table):
        """Load data from database, then show it in the table widget."""

        # Get Employeies Data.
        employeies = db.getAll("select employee from history")
        empolyeiesNames = tool.getEmployeeName(employeies)

        # Show in The Table.
        for employee in empolyeiesNames:
            tool.showEmployeeDataInTable(table, employee)

            
class DashbourdTab():

    # Get the Branch Information.
    def getBranchData(self, objects): # Tool.
        """objects Dict data type\n
        the keys are\n
        < branch >"""

        # Variables.
        branchName = objects['branch']

        # Get.
        branchData = db.getOne("select name, location, admin from branch where name = '{}'".format(branchName))

        if len( branchData ) == empty:
            branchData = ('All Branchies', 'Center', 'System Admin')

        return branchData

    # Calulate.
    def rentScale(self, branch):

        #Variables.
        scale = db.getAll("select * from daily_movments where branch_id = '{}' and type = 'Rent'".format(branch))

        # Output.
        return str( len(scale) )

    def retrieveScale(self, branch):

        #Variables.
        scale = db.getAll("select * from daily_movments where branch_id = '{}' and type = 'Retrieve'".format(branch))

        # Output.
        return str( len(scale) )

    def booksScale(self, branch):

        #Variables.
        scale = db.getAll("select * from history where branch_id = '{}' and actions = 'Add new Book'".format(branch))

        # Output.
        return str( len(scale) )
    
    def clientsScale(self, branch):

        #Variables.
        scale = db.getAll("select * from history where branch_id = '{}' and actions = 'Add new client'".format(branch))

        # Output.
        return str( len(scale) )
    
    def visitorsScale(self, branch):

        #Variables.
        scale = db.getAll("select * from daily_movments where branch_id = '{}'".format(branch))

        # Output.
        return str( len(scale) )
    
    def incomeScale(self, branch):

        #Variables.
        totalIncome = 0
        income = db.getAll("select book_id from daily_movments where branch_id = '{}'".format(branch))
        
        # Calculate.
        for bookPrice in income:
            totalIncome += db.getOne("select price from books where title = '{}'".format(bookPrice))[0]
        
        # Output.
        return str( len(totalIncome) )
    
    # Load the Branch Inormation.
    def loadBranchData(self, objects):
        """objects Dict data type\n
        the keys are\n
        < branch, name, location, admin, title
        rent, retrieve, books, clients, total, visitors, income, outcome>"""

        # Variables.
        branch = objects['branch']
        branchName = objects['name']
        branchLocation = objects['location']
        branchAdmin = objects['admin']
        title = objects['title']
        
        rent = objects['rent']
        retrieve = objects['retrieve']
        books = objects['books']
        clients = objects['clients']
        visitors = objects['visitors']
        

        myObjects = [branchName, branchLocation, branchAdmin, title]


        # Sacels.
        rentScale = self.rentScale(branch)
        retrieveScale = self.retrieveScale(branch)
        booksScale = self.booksScale(branch)
        clientsScale = self.clientsScale(branch)
        visitorsScale = self.visitorsScale(branch)


        # Set Scales.
        rent.setText(rentScale)
        retrieve.setText(retrieveScale)
        books.setText(booksScale)
        clients.setText(clientsScale)
        visitors.setText(visitorsScale)



        # Get Data.
        branchData = self.getBranchData(objects)

        # Load Data.
        dataIndx = 0
        for object in myObjects:

            if object != objects['title']:
                object.setText(branchData[dataIndx])
                dataIndx+=1
            elif object==objects['title']:
                object.setText( str(DateFile.dmyDate))
                


class SettingTab():

    """===== Author ===="""
    # Get Author Data Fields.
    def getAuthorDataFields(self,objects):
        """objects --> dictionary data type \n
        the key in this order\n
        <name, location>"""

        # Variables.
        id = db.generateID("select * from author")
        authorName = objects['name'].text()
        authorLocation = objects['location'].text()

        # Check
        fields = {'Author name':authorName, 'Author location':authorLocation}
        checkResult = tool.checkFields(fields)

        # Output.
        if checkResult==True:
            return (id, authorName, authorLocation)
        else:
            return checkResult

    # Clear Author Data Fields.
    def clearAuthorDataFields(self, objects):
        """objects --> dictionary data type \n
        the key in this order\n
        <name, location>"""
        objects['name'].clear()
        objects['location'].clear()

    # Author Data.
    def fetchAuthorData(self, objects):
        """objects --> dictionary data type \n
        the key in this order\n
        <name, location, branch, employee>"""

        # __init__
        canRun = True

        # Variables.
        authorData = self.getAuthorDataFields(objects)
        branch = objects['branch']
        employee = objects['employee']

        # Check.
        if authorData==False:
            canRun=False

        # Run.
        if canRun==True:
            # Save in Database.
            db.insertManyData("insert into author values(?,?,?)",[authorData])

            # Save Action in History.
            action = {'action':'add new author',
                      'extra':authorData[1],
                      'branch id':branch,
                      'employee id':employee}            
            tool.SaveActionToHistory(action)

            # Clean.
            self.clearAuthorDataFields(objects)

            # Output.
            return authorData[1]


    """==== Add Employee ===="""
    # Check Password for employee in employee fields.
    def checkPassword(self, passwords): #Tool.
        """password --> list of password and repassword"""

        # Variables.
        password = passwords[0]
        repassword = passwords[1]

        if password==repassword:
            return True
        else:
            return False
    
    # Check employee branch.
    def checkEmployeeBranch(self, branchCode): # Tool.
        
        checkResult = True
        check = db.getOne("select code from branch where code = {}".format(branchCode))

        if len(check)==empty:
            checkResult=False
        else:
            checkResult=True

        return checkResult
    

    # Get employee data fields.
    def getEmployeeDataFields(self, objects): # Tool.
        """objects --> dictionary data type \n
        the key in this order\n
        <name, mail, phone, id, periority, branch, password, repassword, current employee, current branch>
        """

        # Variables.
        id = db.generateID("select * from employee")
        date = DateFile.dmyDate
        image = "Client.png"
       
        employeeName = objects['name'].text()
        employeeMail = objects['mail'].text()

        employeePhone = objects['phone'].text()
        employeeID = objects['id'].text()

        employeePeriority = objects['periority'].text()
        employeeBranch = objects['branch'].text()

        employeePassword = objects['password'].text()
        employeeRepassword = objects['repassword'].text()
        passwords = [employeePassword, employeeRepassword]


        # Check.
        fields = {
            'Employee name':employeeName,
            'Employee mail':employeeMail,
            'Employee phone':employeePhone,
            'Employee ID':employeeID,
            'Employee periority':employeePeriority,
            'Employee branch':employeeBranch,
            'Employee password':employeePassword,
            'Employee repassword':employeeRepassword
        }
        checkResult = tool.checkFields(fields)        
        if checkResult==True and self.checkPassword(passwords)==True:
            
            checkBranch = self.checkEmployeeBranch(employeeBranch)
                
            if checkBranch==True:
                return (id,
                    employeeName, employeeMail, employeePhone, date,
                    employeeID, employeePeriority, employeeBranch, employeePassword, image
                )
            else:
                print("There is no Branch code like this {}".format(employeeBranch))
                return False
        else:
            return False
    
    # Clear employee data fields.
    def clearEmployeeDataFields(self, objects): # Tool.
        """objects --> dictionary data type \n
        the key in this order\n
        <name, mail, phone, id, periority, branch, password, repassword, current employee, current branch>
        """

        objects['name'].clear()
        objects['mail'].clear()

        objects['phone'].clear()
        objects['id'].clear()
        
        objects['periority'].clear()
        objects['branch'].clear()
        
        objects['password'].clear()
        objects['repassword'].clear()

    # Fetch Employee Data.    
    def fetchEmployeeData(self, objects):
        """objects --> dictionary data type \n
        the key in this order\n
        <name, mail, phone, id, periority, branch, password, repassword, current employee, current branch>
        """

        # __inti_
        canRun = True

        # Variables.
        currentEmployee = objects['current employee']
        currentBranch = objects['current branch']

        # Get Employee data fields.
        employeeData = self.getEmployeeDataFields(objects)

        # Check.
        if employeeData==False:
            canRun=False

        # Run.
        if canRun==True:

            employeeName = employeeData[1]

            # Add to Database.
            db.insertManyData("insert into employee values(?,?,?,?,?,?,?,?,?,?)",[employeeData])

            # Add permission to employee.
            permissionID = db.generateID("select * from employee_permission")
            db.insertManyData("insert into employee_permission values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",[
                (permissionID, employeeName, 0,0,0,0,0, 1,1,1,0,0, 1,1,0,1,0,0, 0,0,0, 0)
            ])

            # Save action to History.
            action = {'action':'add new employee',
                      'extra':employeeName,
                      'branch id':currentBranch,
                      'employee id':currentEmployee}
            tool.SaveActionToHistory(action)

            # Clean.
            self.clearEmployeeDataFields(objects)

            # Output.
            return employeeName



    """===== Edit Employee ====="""
    # Check Emlpoyee is it in System.
    def checkEmployeeInSystem(self, objects): # Tool.
        """objects dictionary data type.\n
        the keys in this order.\n
        <name, password>"""

        # Variables.
        employeeName = objects['name']
        employeePassword = objects['password']

        # Check Fields.
        fields = {'employee name':employeeName, 'employee password':employeePassword}
        checkResult = tool.checkFields(fields)


        # Check.
        if checkResult==True:
            checkEmployee = db.getOne("select name, password from employee where name = '{}' and Password = '{}'".format(employeeName, employeePassword))

            if len(checkEmployee) == empty:
                print("Wrong !! password or username.")
                return False
            else:
                return True

    # Load employee data to system screen.
    def loadEmployeeDataFields(self, objects): # Tool.
        """objects dictionary data type.\n
        the keys in this order.\n
        <phone, mail, id, periority, branch, password, repassword>
        """

        # Variables.
        employeeName = objects['name']
        employeePassword = objects['password']

        employeePhone = objects['phone']
        employeeMail = objects['mail']
        employeeID = objects['id']

        employeePeriority = objects['periority']
        employeeBranch = objects['branch']

        
        # Load Data.
        employeeData = db.getOne("select phone, mail, national_id, Periority, Branch from employee where name = '{}' and password = '{}'".format(employeeName, employeePassword))


        # Full fields.
        employeePhone.setText(employeeData[0])
        employeeMail.setText(employeeData[1])
        employeeID.setText( str(employeeData[2]) )

        employeePeriority.setText( str(employeeData[3]) )
        employeeBranch.setText( str(employeeData[4]) )

        
    # Commit employee data changes to database.
    def saveEmployeeDataChanges(self, objects): # Tool.
        """objects dictionary data type.\n
        the keys in this order.\n
        <name, phone, mail, id, periority, branch, password, repassword, current branch, current employee>
        """

        # __inti__
        canRun = True
        currentBranch = objects['current branch']
        currentEmployee = objects['current employee']



        # Variables.
        employeeName = objects['name'].text()
        employeePassword = objects['password'].text()

        employeePhone = objects['phone'].text()
        employeeMail = objects['mail'].text()
        employeeID = objects['id'].text()

        employeePeriority = objects['periority'].text()
        employeeBranch = objects['branch'].text()

        employeeRepassword = objects['repassword'].text()
        passwords = [employeePassword, employeeRepassword]


        # Check fields & password .
        fields = {
            'employee name':employeeName,
            'employee password':employeePassword,
            'employee phone':employeePhone,
            'employee mail':employeeMail,
            'employee id':employeeID,
            'employee periority':employeePeriority,
            'employee branch':employeeBranch,
            'employee repassword':employeeRepassword
        }
        checkResult = tool.checkFields(fields)
        checkPassword = self.checkPassword(passwords)


        if checkResult==False:
            canRun=False
        elif checkPassword==False:
            canRun=False

        
        # Run.
        if canRun==True:
            # Update data.
            sqlQuery = """update employee set phone = '{}',
                            mail = '{}',
                            national_id = {},
                            Periority = {},
                            Branch = '{}'
                            where name = '{}' and Password = '{}'""".format(
                            employeePhone, employeeMail,
                            int(employeeID), int(employeePeriority), int(employeeBranch),
                            employeeName, employeePassword
                            )
            db.updateData(sqlQuery)

            # Save Action in History.
            action = {'action':'edit employee', 'extra':employeeName, 'branch id':currentBranch, 'employee id':currentEmployee}
            tool.SaveActionToHistory(action)

            return employeeName
        else:
            return None


    """===== Add Employee Permissions ====="""    

    # Get Book Permissions.
    def getBookPermissions(self, objects): # Tool.
        """objects is a Dict data type\n
        the Keys in this order\n
        < admin, name, all book, add book, edit book, delete book, export book, import book >"""

        # Variables.
        admin = objects['admin'].isChecked()
        employeeName = objects['name']

        allBookP = objects['all book'].isChecked()
        addBookP =  objects['add book']
        editBookP =  objects['edit book']
        deleteBookP =  objects['delete book']
        exportBookP =  objects['export book']
        importBookP =  objects['import book']

        permissions = [addBookP, editBookP, deleteBookP, exportBookP, importBookP]
        permissionsData = []


        # Prossece.
        if allBookP==True or admin==True:
            
            # Ckeck in.
            for check in permissions:
                check = check.setChecked(1)
                permissionsData.append( True )
            
        
        else:
            
            # Check in.
            for check in permissions:
                check = check.isChecked()
                permissionsData.append(check)

        # Save changes.
        sqlQuery = """update employee_permission set 
        add_book = {}, edit_book = {}, delete_book = {}, export_book = {}, import_book = {} 
        where name = '{}'""".format(
            permissionsData[0], permissionsData[1], permissionsData[2], permissionsData[3], permissionsData[4],
            employeeName
        )
        db.updateData(sqlQuery)

        # Output.
        return permissionsData

    # Get Client Permissions.
    def getClientPermissions(self, objects): # Tool.
        """objects is a Dict data type\n
        the Keys in this order\n
        < admin, all client, add client, edit client, delete client, export client, import client >"""

        # Variables.
        admin = objects['admin'].isChecked()
        employeeName = objects['name']

        allClientP = objects['all client'].isChecked()
        addClientP =  objects['add client']
        editClientP =  objects['edit client']
        deleteClientP =  objects['delete client']
        exportClientP =  objects['export client']
        importClientP =  objects['import client']

        permissions = [addClientP, editClientP, deleteClientP, exportClientP, importClientP]
        permissionsData = []


        # Prossece.
        if allClientP==True or admin==True:
            
            # Ckeck in.
            for check in permissions:
                check = check.setChecked(1)
                permissionsData.append( True )
            
        
        else:
            
            # Check in.
            for check in permissions:
                check = check.isChecked()
                permissionsData.append(check)

        # Save changes.
        sqlQuery = """update employee_permission set 
        add_client = {}, edit_client = {}, delete_client = {}, export_client = {}, import_client = {} 
        where name = '{}'""".format(
            permissionsData[0], permissionsData[1], permissionsData[2], permissionsData[3], permissionsData[4],
            employeeName
        )
        db.updateData(sqlQuery)

        # Output.
        return permissionsData
    
    # Get Public Permissions.
    def getPublicPermissions(self, objects): # Tool.
        """objects is a Dict data type\n
        the Keys in this order\n
        < admin, all public, book , client, dashbourd, history, reports, setting >"""

        # Variables.
        admin = objects['admin'].isChecked()
        employeeName = objects['name']

        allPublicP = objects['all public'].isChecked()
        bookP = objects['book']
        clientP = objects['client']
        dashbourdP = objects['dashbourd']
        historyP = objects['history']
        reportsP = objects['reports']
        settingP = objects['setting']
        

        permissions = [bookP, clientP, dashbourdP, historyP, reportsP, settingP]
        permissionsData = []


        # Prossece.
        if allPublicP==True or admin==True:
            
            # Ckeck in.
            for check in permissions:
                check = check.setChecked(1)
                permissionsData.append( True )
            
        
        else:
            
            # Check in.
            for check in permissions:
                check = check.isChecked()
                permissionsData.append(check)

        # Save changes.
        sqlQuery = """update employee_permission set 
        book_tap = {}, client_tap = {}, dashbourd_tap = {}, history_tap = {}, reports_tap = {}, settings_tap = {} 
        where name = '{}'""".format(
            permissionsData[0], permissionsData[1], permissionsData[2], permissionsData[3], permissionsData[4], permissionsData[5],
            employeeName
        )
        db.updateData(sqlQuery)
        
    
    # Get Settings Permissions.
    def getSettingPermissions(self, objects): # Tool.
        """objects is a Dict data type\n
        the Keys in this order\n
        < admin, all setting, add data, add employee, edit employee >"""

        # Variables.
        admin = objects['admin'].isChecked()
        employeeName = objects['name']

        allSettingP = objects['all setting'].isChecked()
        dataP = objects['add data']
        addEmployeeP = objects['add employee']
        editEmployeeP = objects['edit employee']
        
        

        permissions = [dataP, addEmployeeP, editEmployeeP]
        permissionsData = []


        # Prossece.
        if allSettingP==True or admin==True:
            
            # Ckeck in.
            for check in permissions:
                check = check.setChecked(1)
                permissionsData.append( True )
            
        
        else:
            
            # Check in.
            for check in permissions:
                check = check.isChecked()
                permissionsData.append(check)

        # Save changes.
        sqlQuery = """update employee_permission set 
        add_data = {}, add_employee = {}, edit_employee = {} 
        where name = '{}'""".format(
            permissionsData[0], permissionsData[1], permissionsData[2],
            employeeName
        )
        db.updateData(sqlQuery)


        
    
    # Commit and save employee permissions.
    def commitEmployeePermissions(self, objects):
        """objects is a Dict data type\n
        the Keys in this order\n
        < admin, name
        all book, add book, edit book, delete book, export book, import book,
        all client, add client, edit client, delete client, export client, import client,
        all public, book , client, dashbourd, history, reports, setting,
        all setting, add data, add employee, edit employee >"""

        # Variables.
        employeeName = objects['name']

        self.getBookPermissions(objects)
        self.getClientPermissions(objects)
        self.getPublicPermissions(objects)
        self.getSettingPermissions(objects)
        
        # Output.
        return employeeName
        
    """==== Edit Employee Permissions ====="""
    
    # Load employee permissions.
    def loadEmployeePermissions(self, objects): # Tool.
        """objects is a Dict data type\n
        the Keys in this order\n
        < admin, name
        all book, add book, edit book, delete book, export book, import book,
        all client, add client, edit client, delete client, export client, import client,
        all public, book , client, dashbourd, history, reports, setting,
        all setting, add data, add employee, edit employee >"""

        # Variables.
        employeeName = objects['name']
        allPermissions = db.getOne("select * from employee_permission where name = '{}'".format(employeeName))

        bookPermissions = [objects['add book'], objects['edit book'], objects['delete book'], objects['export book'], objects['import book']]
        clientPermissions = [objects['add client'], objects['edit client'], objects['delete client'], objects['export client'], objects['import client']]
        publicPermissions = [objects['book'], objects['client'], objects['dashbourd'], objects['history'], objects['reports'], objects['setting']]
        settingPermissions = [objects['add data'], objects['add employee'], objects['edit employee']]
 

        # Book.
        indx = 2; countChecked = 0;       
        for checkBox in bookPermissions:
            checkBox.setChecked( allPermissions[indx] )

            if allPermissions[indx]==True:
                countChecked+=1

            indx+=1
            

        if countChecked==5:
            objects['all book'].setChecked(True)
            


        # Client.
        countChecked = 0;       
        for checkBox in clientPermissions:
            checkBox.setChecked( allPermissions[indx] )

            if allPermissions[indx]==True:
                countChecked+=1

            indx+=1

        if countChecked==5:
            objects['all client'].setChecked(True)

        # Public.
        countChecked = 0;       
        for checkBox in publicPermissions:
            checkBox.setChecked( allPermissions[indx] )

            if allPermissions[indx]==True:
                countChecked+=1

            indx+=1
            

        if countChecked==6:
            objects['all public'].setChecked(True)
            

        # Setting.
        countChecked = 0;       
        for checkBox in settingPermissions:
            checkBox.setChecked( allPermissions[indx] )

            if allPermissions[indx]==True:
                countChecked+=1
            indx+=1

        if countChecked==3:
            objects['all setting'].setChecked(True)
            
class ProfileTab():

    # Get Total work for user.
    def getTotalWorks(self, username):

        totalWorks = db.getAll("select * from history where employee = '{}' and actions != 'Login'".format(username))

        return str( len(totalWorks) )
    
    # Get user image.
    def getUserImage(self, username):
        if username=='admin':
            return 'Client.png'
        else:
            return db.getOne("select image from employee where name = '{}'".format(username))[0]
        
    # Get Employee or User Data.
    def getProfileData(self, username):
        """objects is Dict date type\n
        the keys in order\n
        < name >"""

        # Variables.
        name = username
        email = 1
        joinData = 2
        totalWorks = self.getTotalWorks(name)
        image = self.getUserImage(name)



        # Get Data.
        if name == 'admin':
            profileData = ('admin', 'admin@system', '', totalWorks, image)

        else:
            userData = db.getOne("select name, mail, date from employee where name = '{}'".format(name))
            print(userData)
            profileData = ( name, userData[email], userData[joinData], totalWorks, image )

        # Output.
        return profileData








