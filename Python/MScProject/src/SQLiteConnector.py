'''
Created on Aug 4, 2014

@author: Jools
'''

import sqlite3
import sys
import os

databasePath = '/home/azureuser/Documents/SensorReadingsFileLog.db'

#Loop through available process arguments
for i in range(1,len(sys.argv)):
    filePath = sys.argv[i]
    sqlString = "INSERT INTO ReadingFiles (FilePath, Uploaded) VALUES ('" + filePath + "', 0)"
    if (os.path.isfile(databasePath)):
        dbConnection = sqlite3.connect(databasePath)
        try:
            with dbConnection:
                dbConnection.execute(sqlString)
        except sqlite3.IntegrityError as e:
            print "SQL Integrity Error, INSERT statement failed, rolling back transaction"
        finally:
            dbConnection.close()
    else:
        print "SensorReadingsFileLog.db not found."