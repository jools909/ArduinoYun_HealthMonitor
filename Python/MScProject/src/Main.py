import os

datafolderPath = '***path of folder that contains data files on sd card***'
dbTableName = 'Sensor1Table'

#Get list of files and sort resultant list
fileList = os.listdir(datafolderPath)
fileList.sort()

#loop through each file in list
for fileOb in fileList:
    sqlString ="INSERT INTO " + dbTableName + " (DateTime, Reading1) VALUES"
    f=open(fileOb, 'r')
    #go through each line of the current file
    for line in f:
        sqlString = sqlString + " ('"
        #loop through each character of the line string
        workingValue = ''
        for letter in line:
            if letter == '=':
                sqlString = sqlString + workingValue + "',"
                workingValue = ''
            elif letter == ',':
                sqlString = sqlString + workingValue + ","
                workingValue = ''
            elif letter == ';':
                sqlString = sqlString + workingValue + ")"
                workingValue = ''
            else:
                workingValue = workingValue + letter