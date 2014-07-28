import os

datafolderPath = '***path of folder that contains data files on sd card***'

#Get list of files and sort resultant list
fileList = os.listdir(datafolderPath)
fileList.sort()

#loop through each file in list
for file in fileList:
  sqlString =""
  f=open(file, 'r')
  #go through each line of the current file
  for line in f:
    