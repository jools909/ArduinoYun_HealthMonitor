'''
Created on Aug 6, 2014

@author: Julian Ostmo
@param currentDBfile: current working .db file (i.e. "20140806.db")
'''

import os
import sys
import WiFiConnection
import DatabaseConnect
import SQLiteDatabaseHandler
import time
import pyodbc

dbFolderPath = '/home/azureuser/Documents/DatabaseFiles/'
if len(sys.argv) > 1:
    currentDBfile = sys.argv[1]
else:
    currentDBfile = ''
cloudDBtableName = 'Sensor1Table'

#Get list of .db files and sort resultant list
fileList = os.listdir(dbFolderPath)
fileList.sort()

#For each .db file in the database folder (except the current working database)
#check and upload any readings with 'Uploaded' = False (0). 
for fileOb in fileList:
    if fileOb != currentDBfile:
        db = SQLiteDatabaseHandler.SQLiteDatabaseHandler(dbFolderPath + fileOb)
        results = db.Select('''SELECT * FROM Readings WHERE Uploaded = 0''')
        
        #If non-uploaded readings are found, an SQL INSERT string is created.
        sqlString = ''
        if results != None:
            sqlString = "INSERT INTO " + cloudDBtableName + " (DateTime, Reading1) VALUES"
            for rows in results:
                sqlString += " ('%s', %s)," % (rows['DateTime'], rows['Reading'])
            sqlString = sqlString[:-1]
        
            #If internet connection is available connect to Cloud database
            #and execute INSERT SQL string.
            wifi = WiFiConnection.WiFiConnection()
            
            sleepCounter = 1
            while wifi.isConnected() == False:
                if sleepCounter == 1:
                    print 'Waiting for WiFi connection'
                else:
                    print '.'
                time.sleep(2*sleepCounter)
                if sleepCounter < 30:
                    sleepCounter += 1
                #wifi = WiFiConnection.WiFiConnection.isConnected()
            print 'WiFi available.'
            
            uploadSuccess = False
            while uploadSuccess == False:
                cloudConnect = DatabaseConnect.DatabaseConnect()
                cloudDB = cloudConnect.Connect()
                if cloudDB != False:
                    print 'Connected to cloud database.'
                    cloudCursor = cloudDB.cursor()
                    try:
                        cloudCursor.execute(sqlString)
                        cloudDB.commit()
                        uploadSuccess == True
                        print 'Executed INSERT SQL.'
                    except pyodbc.Error as e:
                        print e.args
                    cloudDB.close()
                else:
                    print 'Failed to connect to cloud database'
                    time.sleep(1)
            
            #Update SQlite .db fileOb so that 'Uploaded' == True (1)
            if uploadSuccess:
                SQLiteDBupdated = False
                while SQLiteDBupdated == False:
                    updateResult = db.Insert("UPDATE Readings SET Uploaded = 1 WHERE Uploaded = 0")
                    if updateResult:
                        SQLiteDBupdated = True
                        print 'SQLite database updated.'
        else:
            print 'All readings in ' + fileOb + ' have already been uploaded.'