# DATABASE CLASS
import sqlite3

from numpy import empty


"""=================================================
================== Sqlite3 ======================"""
class ConnectSqlite3():
    
    def __init__(self):
        
        # Connect Between Database and Programe.
        self.db = sqlite3.connect("Library_Database.db")
        self.cur = self.db.cursor()


    # Generate ID
    def generateID(self,sqlQuery):
        """Generate ID for the Table's ROW.
        \nsqlQuery is like 'select * from table'."""

        if len(sqlQuery) != 0:
            # Get ID number.
            id = len( self.getAll(sqlQuery) ) +1

            # Check is There another id same and fix it
            anotherID = len( self.getAll(sqlQuery+" where id = '{}'".format(id)) )
            if anotherID > 0:
                id+=1

            return id

        else:
            print("We Connot do this operator.")

    
    # insert  many data into database
    def insertManyData(self,sql,data):
        """Insert a Many data More then > 3.
        \nYou may use (?,?,?) for example, then pass the argument data with your data."""
        
        if len(sql) != 0 and len(data) != 0:
            self.cur.executemany(sql,data)
            self.db.commit()
        
        else:
            print("We cannot do the operator!!.")

    #insert one thing to database.
    def insertOneData(self,sql,data):
        """Insert one thing to database.
        \nyou shoud pass data argument."""

        if len(sql) != 0 and len(data) != 0:
            self.cur.execute(sql,data)
            self.db.commit()
        else:
            print("We cannot do the operator!!.")

    # Update table in database.
    def updateData(self, sql):
        """Update data into its table
        \nYou may use update table set data = value where exprition for example, then pass the argument data with your data."""
        
        if len(sql) != empty:
            self.cur.execute(sql)
            self.db.commit()
        
        else:
            print("We cannot do the operator!!.")

    
    # Delete table in database.
    def deleteData(self, sql):
        """Delete data into its table
        \nYou may use <delete from tableName where name = value> this query,
        then pass the argument data with your data."""
        
        if len(sql) != empty:
            self.cur.execute(sql)
            self.db.commit()
        
        else:
            print("We cannot do the operator!!.")
    
    
    # Get one row of data from database.
    def getOne(self,sql):
        """Fetch one data from database."""

        if len(sql) != 0 :
            self.cur.execute(sql)
            data = self.cur.fetchone()

            if data != None:
                return data
            
            else:
                return ()

    # Get one row of data from database.
    def getAll(self,sql):
        """Fetch Many data from database."""

        if len(sql) != 0 :
            self.cur.execute(sql)
            data = self.cur.fetchall()

            if data != None:
                return data
            
            else:
                return ()


if __name__ == '__main__':
    ConnectSqlite3()