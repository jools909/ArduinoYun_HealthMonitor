'''
Created on Aug 18, 2014

@author: Julian Ostmo
@param SQLiteDatabase: (First script parameter) File name of current .db SQLite database.f  
@param sqlString: (Second script parameter) SQL INSERT query from Arduino readings.

Script run by the Arduino to INSERT sensor readings into the SQLite database.
'''
import sys
import SQLiteDatabaseHandler

SQLiteDBpath = '/mnt/sd/SQLiteDatbases/'
SQLiteDatabase = sys.argv[1]
sqlString = sys.argv[2]

sqliteDB = SQLiteDatabaseHandler.SQLiteDatabaseHandler(SQLiteDBpath + SQLiteDatabase)
sqliteDB.Insert(sqlString)