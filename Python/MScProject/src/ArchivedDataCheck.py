'''
Created on Aug 6, 2014

@author: Julian Ostmo
@param currentDBfile: current working .db file (i.e. "20140806.db")
'''

import sqlite3
import os
import sys
import WiFiConnection
import DatabaseConnect
import time
import pyodbc

dbFolderPath = '/home/azureuser/Documents/DatabaseFiles/'
currentDBfile = sys.argv[1]
cloudDBtableName = 'Sensor1Table'

#Get list of .db files and sort resultant list
fileList = os.listdir(dbFolderPath)
fileList.sort()

#For each .db file in the database folder (except the current working database)
#check and upload any readings with 'Uploaded' = False (0). 
for fileOb in fileList:
    if fileOb != currentDBfile:
        db = sqlite3.connect(dbFolderPath + fileOb)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Readings WHERE Uploaded = 0''')
        row = cursor.fetchone()
        sqlString = ''
        
        #If non-uploaded readings are found, an SQL INSERT string is created.
        if row != None:
            sqlString = "INSERT INTO " + cloudDBtableName + " (DateTime, Reading1) VALUES"
            for rows in cursor:
                sqlString += " ('%s', %s)," % (rows['DateTime'], rows['Reading1'])
            sqlString = sqlString[:-1]
        db.close()
        
        #If internet connection is available connect to Cloud database
        #and execute INSERT SQL string.
        wifi = WiFiConnection.WiFiConnection
        
        while wifi.isConnected() == False:
            time.sleep(1)
        cloudDB = DatabaseConnect.DatabaseConnect.Connect()
        if cloudDB != False:
            cloudCursor = cloudDB.cursor()
            try:
                cloudCursor.execute(sqlString)
                cloudDB.commit()
            except pyodbc.Error as e:
                print e.args
            
                
            
            
            
            
            
            
            
            
            
        