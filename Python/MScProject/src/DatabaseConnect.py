'''
Created on 23 Jul 2014

@author: Jools
'''
import pyodbc

class DatabaseConnect:
    
    def Connect(self):
        #Connect to Cloud Database
        #Tries to connect to the cloud database
        #Returns a connection variable if connects, else returns false.
        try:
            conn = pyodbc.connect('DRIVER={SQL Server Native Client 10.0};SERVER=h9flrbpsdu.database.windows.net;DATABASE=SensorReadingsDB;UID=jools909@h9flrbpsdu;PWD=SPL_ash2')
        except pyodbc.Error:
            return False
        else:
            return conn