'''
Created on Aug 6, 2014

@author: azureuser
'''

#Tests SQLite database connection class

import SQLiteDatabaseHandler as SQL

db = SQL.SQLiteDatabaseHandler('/tmp/test.db')
createDB = db.Insert('''CREATE TABLE sensordata (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                        DateTime DATETIME NOT NULL,
                                        Sensor1 INT NOT NULL,
                                        Uploaded INT NOT NULL)''')
if createDB:
    insertData = [("'2014-05-06 12:13:14'", 1234, 0), 
                    ("'2014-05-07 14:15:16'", 4321, 0), 
                    ("'2014-05-08 16:17:18'", 6789, 0)]
    insertResult = True
    for segment in insertData:
        sql = "INSERT INTO sensordata (DateTime, Sensor1, Uploaded) VALUES (%s, %s, %s)" % segment
        insert = db.Insert(sql)
        if insert == False:
            insertResult = False
    if insertResult:
        rows = db.Select("SELECT * FROM sensordata WHERE Uploaded = 0")
        if rows != False:
            if not rows:
                print "Empty"
            else:
                for results in rows:
                    print results
        else:
            print "SELECT query failed"
    else:
        print "INSERT query failed"
else:
    print "CREATE TABLE query failed"


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