'''
Created on 4 Sep 2014

@author: Jools
'''
import sys
import os
import SQLiteDatabaseHandler

SQLiteDBpath = '/mnt/sda1/arduino/databases/'
SQLiteDatabase = sys.argv[1]
sqlString = sys.argv[2]

#check if working .db file exists
if not os.path.isfile(SQLiteDBpath + SQLiteDatabase):
    #working .db file doesn't exist, must perform CREATE DATEBASE SQLite Query
    db = SQLiteDatabaseHandler.SQLiteDatabaseHandler(SQLiteDBpath + SQLiteDatabase)
    db.Insert('''CREATE TABLE sensordata (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                          DateTime DATETIME NOT NULL, 
                                          Sensor1 TEXT NOT NULL,
                                          Uploaded INT NOT NULL)''')

sqliteDB = SQLiteDatabaseHandler.SQLiteDatabaseHandler(SQLiteDBpath + SQLiteDatabase)
result = sqliteDB.Insert(sqlString)
print result