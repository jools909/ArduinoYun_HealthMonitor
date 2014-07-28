import os

datafolderPath = '***path of folder that contains data files on sd card***'

#Get list of files and sort resultant list
fileList = os.listdir(datafolderPath)
fileList.sort()

#loop through each file in list
for fileOb in fileList:
    sqlString =""
    f=open(fileOb, 'r')
    #go through each line of the current file
    for line in f:
        