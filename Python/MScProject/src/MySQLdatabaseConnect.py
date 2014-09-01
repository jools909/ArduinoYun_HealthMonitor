'''
Created on Aug 29, 2014

@author: Julian Ostmo
'''

import MySQLdb

db = MySQLdb.connect("eu-cdbr-azure-north-b.cloudapp.net", "b968f50cabc1d1", "f61f8258", "ArduinoMySQL")

cursor = db.cursor()

sqlString = "SELECT * FROM sensordata"

try:
    cursor.execute(sqlString)
    results = cursor.fetchall()
    for row in results:
        ReadingID = row[0]
        DateTime = row[1]
        Sensor1 = row[2]
        print "ReadingID= %s, DateTime= %s, Sensor1= %s" % (ReadingID,DateTime,Sensor1)
except:
    print "Error: unable to fetch data."
finally:
    db.close()
