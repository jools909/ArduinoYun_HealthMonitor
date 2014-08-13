'''
Created on Aug 6, 2014

@author: Julian
'''
import sqlite3

class SQLiteDatabaseHandler():
    '''
    @param database: path of .db file
    '''

    def __init__(self, database):
        self.database = database
        
    
    def Connect(self):
        '''
        Connect to .db database
        Returns a connection variable if connects, else returns false.
        '''
        try:
            conn = sqlite3.connect(self.database)
        except sqlite3.Error:
            return False
        else:
            return conn
    
    def Insert(self, sqlString):
        '''
        Executes an INSERT/UPDATE/DELETE/REPLACE SQL statement.
        @param sqlString: SQL INSERT statement.
        @return: boolean whether successfully executed
        '''
        db = self.Connect()
        result = False
        if db != False:
            result = True
            try:
                with db:
                    db.execute(sqlString)
            except sqlite3.Error:
                result = False
            finally:
                db.close()
        return result
    
    def Select(self, sqlString):
        '''
        Executes a SELECT SQL statement.
        @param sqlString: SQL SELECT statement
        @return: either arraylist of rows or false.
        '''
        db = self.Connect()
        result = False
        rowArraylist = []
        if db != False:
            result = True
            try:
                db.row_factory = sqlite3.Row
                cursor = db.cursor()
                cursor.execute(sqlString)
                for results in cursor:
                    rowArraylist.extend([results])
            except sqlite3.Error:
                result = False
            finally:
                db.close()
        if result == False:
            return False
        else:
            return rowArraylist
    
        