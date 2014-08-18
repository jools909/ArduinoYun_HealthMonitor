'''
Created on Aug 18, 2014
@author: Julian Ostmo
@param CurrentSQLiteDB: First script parameter, path of current SQLite database. 

A looping script that reads a SQLite database and uploads it
to a cloud-based MS SQL database. If an error occurs the script waits and
then restarts the upload loop.
'''

import sys
import time
import SQLiteDatabaseHandler
import WiFiConnection
import DatabaseConnect
import pyodbc

#First checks if parameter has been passed to script.
#If not, script must be restarted with parameter.
if len(sys.argv) > 1:
    CurrentSQLiteDB = sys.argv[1]
    
    dbFolderPath = '/home/azureuser/Documents/DatabaseFiles/'
    cloudDBtableName = 'Sensor1Table'
    wifiCounter = 1
    
    while True:
        #Try to connect to SQLite database 'CurrentSQLiteDB' and execute SELECT query,
        #if an exception occurs 'False' is return, so sleep for 1 sec and restart loop. Else continue.
        sqlitedb = SQLiteDatabaseHandler.SQLiteDatabaseHandler(dbFolderPath + CurrentSQLiteDB)
        dataToUpload = sqlitedb.Select('''SELECT * FROM Readings WHERE Uploaded = 0''')
        if dataToUpload != False:
            if dataToUpload:
                #Data available to upload, iterate through returned data to make INSERT SQL string.
                sqlString = "INSERT INTO " + cloudDBtableName + " (DateTime, Reading1) VALUES"
                for rows in dataToUpload:
                    sqlString += " ('%s', %s)," % (rows['DateTime'], rows['Reading'])
                sqlString = sqlString[:-1]
                sqlString = str(sqlString)
                
                #Check WiFi connection available,
                #If not, wait for 2 seconds, increasing to a maximum of 60 seconds if unavailable.
                wifi = WiFiConnection.WiFiConnection()
                if wifi.isConnected():
                    #WiFi connection available, resetting wifiCounter.
                    wifiCounter = 1
                    
                    #Try connecting to cloud database
                    cloudConnect = DatabaseConnect.DatabaseConnect()
                    cloudDB = cloudConnect.Connect()
                    if cloudDB != False:
                        
                        #Perform INSERT SQL query on cloud database.
                        cloudCursor = cloudDB.cursor()
                        uploadSuccess = False
                        try:
                            cloudCursor.execute(sqlString)
                            cloudDB.commit()
                            uploadSuccess = True
                        except pyodbc.Error as e:
                            print 'Error: ' + str(e.args)
                        finally:
                            cloudDB.close()
                        
                        if uploadSuccess:
                            
                            #UPDATE query to SQLite database to change Uploaded from 0 to 1.
                            for rows in dataToUpload:
                                rowUpdated = False
                                while rowUpdated == False:
                                    rowQuery = sqlitedb.Insert(
                                        '''UPDATE Readings SET Uploaded = 1 WHERE ID = %s''' % rows['ID'])
                                    if rowQuery:
                                        rowUpdated = True
                                    else:
                                        print 'Error: SQLite database UPDATE query failed.'
                                        #Wait 1 second and try to Update SQLite database again.
                                        #(Cannot restart loop as readings would then be 
                                        #duplicated on cloud database)
                                        time.sleep(1)
                            #Loop cycle completed successfully.
                            print 'Loop cycle completed successfully.'
                        else:
                            print 'Error: Cloud database INSERT query failed.'
                            #Wait 1 second and restart while loop
                            time.sleep(1)
                    else:
                        print 'Error: Failed to connect to cloud database'
                        #Wait 1 second and restart while loop
                        time.sleep(1)
                else:
                    print 'Error: No internet connection. Waiting for connection.'
                    #Wait for 2-60 seconds.
                    time.sleep(2*wifiCounter)
                    wifiCounter += 1
            else:
                print 'Error: No data to Upload. Waiting for new data.'
                #Wait 1 second and restart while loop
                time.sleep(1)
        else:
            print 'Error: SQLite database connection or SELECT query error.'
            #Wait 1 second and restart while loop
            time.sleep(1)
else:
    print 'Error: No parameter given, path of current SQLite database required.'