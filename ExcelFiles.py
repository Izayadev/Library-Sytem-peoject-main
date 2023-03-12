# This class is to work with excel files
from numpy import empty_like
from xlsxwriter import *
import Database, Tools
import DateFile as date
db = Database.ConnectSqlite3()


class BookReports():

        
    def exportBookReport(self, objects):
        """The list of books in book tab exported as excel file.\n
        objects are --> employee id, branch id"""

        # VARIABLES
        currentDate = date.dofmDate
        employee = objects['employee id']
        branch = objects['branch id']

        # GET
        bookData = db.getAll("select code, title, category_id, author_id, price from books")
        
        
        """=========== EXCEL FILE SETTING ============="""
        # SET FILE
        excelFile = Workbook('Book Export Report ('+str( currentDate )+' ).xlsx')
        thisSheet = excelFile.add_worksheet()

        # Add Formats
        bold = excelFile.add_format({'bold':1})
        money_format = excelFile.add_format({"num_format": '$#,##0'})
        
        # Format Columns
        thisSheet.set_column(0,3,18)

        # Set Headers
        thisSheet.write('A1','Book Code', bold)
        thisSheet.write('B1','Book Title', bold)
        thisSheet.write('C1','Category', bold)
        thisSheet.write('D1','Author', bold)
        thisSheet.write('E1','Price', bold)


        # Insert data from database to excel file
        for row, form in enumerate(bookData):
            row+=1
            for col, item in enumerate(form):
                # Get real data name for category and author
    
                if col==4:
                    thisSheet.write(row, col, item, money_format)
                    
                else:
                    thisSheet.write(row, col, item)


        # Close Excel file to save
        excelFile.close()

        # Save action to history
        if branch == Tools.adminAccess:
            thisData = {'employee id':"Admin", 'branch id':"Admin", 'action':"export book's list", 'extra':'from Book tab'} 
        else:
            thisData = {'employee id':employee, 'branch id':branch, 'action':"export book's list", 'extra':'from Book tab'} 

        Tools.SaveActionToHistory(thisData)

class ClientReports():

    def exportClientsList(self):
        """The list of clients in client tab exported as excel file."""

        # VARIABLES
        currentDate = date.dofmDate
        

        # GET
        clientData = db.getAll("select name, mail, phone, national_id from clients")
        
        
        """=========== EXCEL FILE SETTING ============="""
        # SET FILE
        excelFile = Workbook('Cleints Export List ('+str( currentDate )+' ).xlsx')
        thisSheet = excelFile.add_worksheet()

        # Add Formats
        bold = excelFile.add_format({'bold':1})
        # money_format = excelFile.add_format({"num_format": '$#,##0'})
        
        # Format Columns
        thisSheet.set_column(0,3,20)

        # Set Headers
        thisSheet.write('A1','Client Name', bold)
        thisSheet.write('B1','Client Mail', bold)
        thisSheet.write('C1','Client Phone', bold)
        thisSheet.write('D1','Client ID', bold)


        # Insert data from database to excel file
        for row, form in enumerate(clientData):
            row+=1
            for col, item in enumerate(form):
                
                thisSheet.write(row, col, item)

                


        # Close Excel file to save
        excelFile.close()

class HistoryReports():

    def exportList(self):
        """The list of actions in history tab exported as excel file."""

        # VARIABLES
        currentDate = date.dofmDate
        

        # GET
        historyData = db.getAll("select employee, actions, branch_id, date, extra from history")
        
        
        """=========== EXCEL FILE SETTING ============="""
        # SET FILE
        excelFile = Workbook('History Actions List ('+str( currentDate )+' ).xlsx')
        thisSheet = excelFile.add_worksheet()

        # Add Formats
        bold = excelFile.add_format({'bold':1})
        # money_format = excelFile.add_format({"num_format": '$#,##0'})
        
        # Format Columns
        thisSheet.set_column(0,3,20)

        # Set Headers
        thisSheet.write('A1','Employee', bold)
        thisSheet.write('B1','Actions', bold)
        thisSheet.write('C1','Branch', bold)
        thisSheet.write('D1','Date', bold)
        thisSheet.write('E1','Extra', bold)


        # Insert data from database to excel file
        for row, form in enumerate(historyData):
            row+=1
            for col, item in enumerate(form):
                
                thisSheet.write(row, col, item)

                


        # Close Excel file to save
        excelFile.close()

class ReportsTab():

    def exportBooksReport(self):
        """The list of Books in Reports tab exported as excel file."""

        # VARIABLES
        currentDate = date.dofmDate
    
        # GET
        historyData = db.getAll("select code, title, category_id, author_id Branch, quantity from books")
        
        
        """=========== EXCEL FILE SETTING ============="""
        # SET FILE
        excelFile = Workbook('Report of All Books ('+str( currentDate )+' ).xlsx')
        thisSheet = excelFile.add_worksheet()

        # Add Formats
        bold = excelFile.add_format({'bold':1})
        # money_format = excelFile.add_format({"num_format": '$#,##0'})
        
        # Format Columns
        thisSheet.set_column(0,3,18)

        # Set Headers
        thisSheet.write('A1','code', bold)
        thisSheet.write('B1','Title', bold)
        thisSheet.write('C1','Category', bold)
        thisSheet.write('D1','Author', bold)
        thisSheet.write('E1','Branch', bold)
        thisSheet.write('F1','Quantity', bold)


        # Insert data from database to excel file
        for row, form in enumerate(historyData):
            row+=1
            for col, item in enumerate(form):
                
                thisSheet.write(row, col, item)

                


        # Close Excel file to save
        excelFile.close()

    def exportClientsReport(self):
        """The list of clients in client report tab exported as excel file."""

        # VARIABLES
        currentDate = date.dofmDate
        

        # GET
        clientData = db.getAll("select national_id, name, mail, phone from clients")
        clientsBooks = Tools.getClientBooks(clientData)
        
        """=========== EXCEL FILE SETTING ============="""
        # SET FILE
        excelFile = Workbook('Report about Clients ('+str( currentDate )+').xlsx')
        thisSheet = excelFile.add_worksheet()

        # Add Formats
        bold = excelFile.add_format({'bold':1})
        # money_format = excelFile.add_format({"num_format": '$#,##0'})
        
        # Format Columns
        thisSheet.set_column(0,3,20)

        # Set Headers
        thisSheet.write('A1','Client ID', bold)
        thisSheet.write('B1','Client Name', bold)
        thisSheet.write('C1','Client Mail', bold)
        thisSheet.write('D1','Client Phone', bold)
        thisSheet.write('E1','Client Books', bold)


        # Insert data from database to excel file
        for row, form in enumerate(clientData):
            row+=1
            for col, item in enumerate(form):
                
                thisSheet.write(row, col, item)

                # Get Books.
                if col==4:
                    thisSheet.write(row, col, clientsBooks[row])


                


        # Close Excel file to save
        excelFile.close()

    def exportEmployeiesReport(self, tableData):
        """The list of Employeies in employee report tab exported as excel file."""

        # VARIABLES
        currentDate = date.dofmDate
        

        
        """=========== EXCEL FILE SETTING ============="""
        # SET FILE
        excelFile = Workbook('Report about Employeies ('+str( currentDate )+').xlsx')
        thisSheet = excelFile.add_worksheet()

        # Add Formats
        bold = excelFile.add_format({'bold':1})
        # money_format = excelFile.add_format({"num_format": '$#,##0'})
        
        # Format Columns
        thisSheet.set_column(0,3,20)

        # Set Headers
        thisSheet.write('A1','Employee Name', bold)
        thisSheet.write('B1','Employee ID', bold)
        thisSheet.write('C1','Action', bold)
        thisSheet.write('D1','Date', bold)
        thisSheet.write('E1','Branch', bold)


        # Insert data from database to excel file
        for row, form in enumerate(tableData):
            row+=1
            for col, item in enumerate(form):
                
                thisSheet.write(row, col, item)


                


        # Close Excel file to save
        excelFile.close()
        
   


































