'''
Created on Aug 29, 2014

@author: Julian Ostmo
'''

import MySQLdb

class MySQLdatabaseConnect:
    
    def Connect(self):
        #Tries to connect to the cloud MySQL database running on Linux virtual machine
        #Returns a connection object if connects, else returns false.
        try:
            conn = MySQLdb.connect("joolsubuntu.cloudapp.net", "azureuser", "SPL_ash2", "ArduinoMySQL")
        except MySQLdb.Error:
            return False
        else:
            return conn