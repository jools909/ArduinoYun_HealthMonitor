'''
Created on 5 Sep 2014

@author: Jools
'''

import sys
import SQLiteDatabaseHandler

SQLiteDBpath = '/mnt/sda1/arduino/databases/'
SQLiteDatabase = sys.argv[1]

sqliteDB = SQLiteDatabaseHandler.SQLiteDatabaseHandler(SQLiteDBpath + SQLiteDatabase)
results = sqliteDB.Select('''SELECT * FROM sensordata WHERE Uploaded = 0''')

if(results != False):
    row = results[len(results)-1]
    print row['DateTime'] 
    print row['Sensor1']
else:
    print "Empty"
