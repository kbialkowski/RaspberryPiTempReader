#! /usr/bin/python
from classes.ds18b20 import DS18B20
from classes.dht11 import DHT11
from classes.dataaccess import DataAccess


try:

    ds = DS18B20()
    dataDS = ds.pobieranieDanych()  
    dht11 = DHT11()
    dataDHT = dht11.pobieranieDanych()
        
    ds.zapisDanych(dataDS)
    dht11.zapisDanych(dataDHT)

except Exception as e:  
    
    print e
    print type(e)
