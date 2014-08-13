'''
Created on 23 Jul 2014

@author: Jools
'''
import urllib2

class WiFiConnection:   
    
    def isConnected(self):
        #Tests internet connection by attemping to connect to www.google.com
        #Returns True if able to connect.
        try:
            urllib2.urlopen("http://www.google.com").close()
        except urllib2.URLError:
            return False
        else:
            return True