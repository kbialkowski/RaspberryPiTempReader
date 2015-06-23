#! /usr/bin/python
from czujnik import Czujnik 
from decimal import Decimal
from classes.dataaccess import DataAccess


class DS18B20(Czujnik):
    
    data = {}
    da = None
    
    def __init__(self):
        self.nazwa = "DS18B20"
        self.da = DataAccess()
        
        
    def zapisDanych(self,data):
        
        data = self.pobieranieDanych()        
        sql = "insert into smash_test.temperature(temp1,temp2,hum1,hum2,iteration,sensor) values(%s,%s,%s,%s,%s,%s);"
        parameters = (data["temp1"],data["temp2"],data["hum1"],data["hum2"],data["i"],data["sensor"])
        self.da.execute(sql,parameters);
        
        
    def pobieranieDanych(self):    
        
        sensor_1 = "/sys/bus/w1/devices/28-00000540f37d/w1_slave"
        sensor_2 = "/sys/bus/w1/devices/28-00000626d753/w1_slave"
        temp_1 = self.odczytajCzujnik(sensor_1)
        temp_2 = self.odczytajCzujnik(sensor_2)
        
        self.data["temp1"] = temp_1
        self.data["temp2"] = temp_2 
        self.data["sensor"] = self.nazwa
        self.data["hum1"] = 0;
        self.data["hum2"] = 0;
        self.data["i"]=0;                
        
        if self.data["temp1"]<=0 or self.data["temp2"]<=0:
            raise Exception("blad DS18B20 temp1:" + str(self.data["temp1"]) + " temp2:"+ str(self.data["temp2"]) );
        
        return self.data
        
        
    def odczytajCzujnik(self,sensor):
        
        sensorFile = open(sensor, "r")
        lines = sensorFile.readlines()
        sensorFile.close()
        equals_pos = lines[1].find("t=")-1
        tempData = lines[1][equals_pos+3:]
        tempC = round(Decimal(tempData)/1000,2)
        
        return tempC
        
        