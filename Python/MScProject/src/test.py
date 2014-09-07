'''
Created on Aug 6, 2014

@author: azureuser
'''

#Tests SQLite database connection class


import MySQLdatabaseConnect as MySQL
import MySQLdb

'''db = SQL.SQLiteDatabaseHandler('C:/Users/Jools/Documents/MSc Project/test.db')
createDB = db.Insert(CREATE TABLE sensordata (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                        DateTime DATETIME NOT NULL,
                                        Sensor1 INT NOT NULL,
                                        Uploaded INT NOT NULL))
'''

db = MySQL.MySQLdatabaseConnect().Connect()

if db != False:
    sql = "INSERT INTO sensordata (DateTime, Sensor1) VALUES "
    for number in range(3600):
        sql = sql + " ('2014-05-06 12:13:14', %s)," % number
    sql = sql[:-1]
    print sql
    try:
        c = db.cursor()
        c.execute(sql)
        print "success"
    except MySQLdb.Error:
        print "INSERT failed."
    finally:
        db.close()
        print "finsihed"
else:
    print "Failed to connect"


#Tests Wifi Connection class
'''
import WiFiConnection

wifi = WiFiConnection.WiFiConnection()

print wifi.isConnected()
'''

#Tests DNS-less connection to Cloud DB
'''
import pyodbc

try:
    conn = pyodbc.connect('DRIVER=FreeTDS;SERVER=h9flrbpsdu.database.windows.net;PORT=1433;DATABASE=SensorReadingsDB;UID=jools909@h9flrbpsdu;PWD=SPL_ash2;TDS_Version=7.2;')
except pyodbc.Error as e:
    print 'Failed'
    print e.args
    #return False
else:
    print 'Connected'
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Sensor1Table (DateTime, Reading1) VALUES ('2014-01-12T22:12:11',1256), ('2014-12-10T22:10:12', 1257)")
        conn.commit()
        print "Success!!!"
    except pyodbc.Error as e:
        print 'Executing of SQL failed'
        print e.args
    finally:
        conn.close()
    #return conn
'''

'''
import DatabaseConnect

dbConn = DatabaseConnect.DatabaseConnect()
while dbConn.Connect() == False:
    print 'Failed to connect'
print 'Connected'
'''