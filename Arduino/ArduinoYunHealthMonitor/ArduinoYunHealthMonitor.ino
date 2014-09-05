// Author: Julian Ostmo
// Date: 29/08/2014

#include <Wire.h>
#include <Console.h>
#include <Process.h>
//MinIMU-9 libraries
#include <L3G.h>
#include <LSM303.h>
//RTC library
#include "RTClib.h"

//RTC and IMU variables
RTC_DS1307 rtc;
L3G gyro;
LSM303 compass;

String currentSQLiteDB;
Process archivePY;
Process dataUploadPY;

void setup () {
  Serial.begin(9600);
  Bridge.begin();
  Console.begin();
  Wire.begin();
  rtc.begin();
  
  //give linux processor 10 seconds to initialize
  Serial.println("Waiting for Linux processor");
  delay(10000);
  Serial.println("Ready");
  
  char SQLdb[15];
  sprintf(SQLdb, "%s.db%c", getDate(), '\0');
  String SQLdbString(SQLdb);
  Serial.println(SQLdbString);
  currentSQLiteDB = SQLdbString;
  Serial.println(currentSQLiteDB);
  
  //run ArchivedDataCheck.py
  archivePY.begin("python");
  archivePY.addParameter("/mnt/sda1/arduino/scripts/ArchivedDataCheck.py");
  archivePY.addParameter(SQLdbString);
  archivePY.runAsynchronously();
  
  //Initialize IMU sensors
  gyro.init();
  gyro.enableDefault();
  compass.init();
  compass.enableDefault();
}

void loop () {
  //get readings from IMU sensor
  gyro.read();
  compass.read();
  char IMUreadings[80];
  sprintf(IMUreadings, "%d,%d,%d,%6d,%6d,%6d,%6d,%6d,%6d%c",
    (int)gyro.g.x, (int)gyro.g.y, (int)gyro.g.z,
    compass.a.x, compass.a.y, compass.a.z,
    compass.m.x, compass.m.y, compass.m.z,'\0');

  //INSERT sensor data into SQLite database
  Process SQLiteDB;
  SQLiteDB.begin("python");
  SQLiteDB.addParameter("/mnt/sda1/arduino/scripts/ArduinoSQLiteConnector.py");
  //.db name parameter
  Serial.print("Process archivePY: ");
  SQLiteDB.addParameter(currentSQLiteDB);
  //sql insert string parameter
  char sqlChar[200];
  sprintf(sqlChar, "INSERT INTO sensordata (DateTime, Sensor1, Uploaded) VALUES ('%s', '%s', 0)%c",
    getDateTime(), IMUreadings, '\0');
  String sqlString(sqlChar);
  SQLiteDB.addParameter(sqlString);
  SQLiteDB.runAsynchronously();
  Serial.println(sqlString);
  
  //Check if ArchivedDataCheck.py is running
  if(!archivePY.running()){
    //Check if DataUpload.py is running
    if(!dataUploadPY.running()){
      //DataUpload.py and ArchivedDataCheck.py are not running, thus run DataUpload.py
      dataUploadPY.begin("python");
      dataUploadPY.addParameter("/mnt/sda1/arduino/scripts/DataUploader.py");
      dataUploadPY.addParameter(currentSQLiteDB);
      dataUploadPY.runAsynchronously();
    } else {
      Serial.println("Process dataUploadPY is already running.");
    }
  } else {
    Serial.println("Process archivePY is still running.");
  }
  Serial.println();
  //wait 1 second before looping
  delay(1000);
}

//returns a char array of todays date as 'yyyymd' or 'yyyymmdd'
char *getDate () {
  DateTime now = rtc.now();
  
  static char currentDate[9];
  sprintf(currentDate, "%i%i%i", now.year(), now.month(), now.day());
  return currentDate;
}

//returns a char array of todays data and time as 'yyyy-mm-dd hh:mm:ss'
char *getDateTime () {
  DateTime now = rtc.now();
  
  static char currentDateTime[25];
  sprintf(currentDateTime, "%i-%i-%i %i:%i:%i",
      now.year(), now.month(), now.day(),
      now.hour(), now.minute(), now.second());
  return currentDateTime;
}
