#! /usr/bin/python
from czujnik import Czujnik 
import RPi.GPIO as GPIO
import time
from classes.dataaccess import DataAccess

class DHT11(Czujnik):
    
    da = None
    
    
    def __init__(self):
        self.nazwa = "DHT11"
        self.da = DataAccess()
        
    def bin2dec(self,string_num): # binary -> decimal.
        return int(string_num, 2)       
        

    def pobieranieDanych(self):
        
        i = 0
    
        while True:
            dataTemp = self.odczytTemp()

            if isinstance(dataTemp, dict):
                dataTemp["i"] = i;
                dataTemp["sensor"] = "DHT11";

                return dataTemp
                break;
            else:    
                i=i+1;
                #print i;
                time.sleep(2);

        
    def odczytTemp(self):
        
        resultData = {}# result table
        data = [] 

        gpio = 17;

        GPIO.setmode(GPIO.BCM)

		#to enable sensor put high state for 25ms then low for 20ms
        GPIO.setup(gpio,GPIO.OUT)  
        GPIO.output(gpio,GPIO.HIGH) # high 1
        time.sleep(0.025) #25 ms
        GPIO.output(gpio,GPIO.LOW) #  low 0
        time.sleep(0.02) #20 ms.
      
        
        GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Change the pin to read mode

        for i in range(0,500): # 501 times
            data.append(GPIO.input(gpio)) # read a bit from the GPIO  
        
        GPIO.cleanup()
        
        bit_count = 0
        tmp = 0
        count = 0
        HumidityBit = ""
        TemperatureBit = ""
        crc = ""
     
        
        try: 
           while data[count] == 1: # as long as you read a 1
              tmp = 1
              count = count + 1 # count how many 1

           #print(data); 

           for i in range(0, 32): # do this 33 times
              bit_count = 0 # reset the bit count each time

              while data[count] == 0: # as long as a 0 is read
                 tmp = 1
                 count = count + 1 # move on to the next bit

              while data[count] == 1: # as long as a 1 is read
                 bit_count = bit_count + 1 # count how many 1s in a row
                 count = count + 1 # move on to the next bit

              if bit_count > 3: # if there were mote than 3 * 1-bits in a row
                 if i>=0 and i<8: # if we're in the first byte
                    HumidityBit = HumidityBit + "1" # append a 1 to the humidity bitstring
                 if i>=16 and i<24: # if we're in the 3rd byte
                    TemperatureBit = TemperatureBit + "1" # add a 1 to the temperature bitstring
              else: # if there weren't at least 3 * 1-bits
                 if i>=0 and i<8: # if we're in the first byte
                    HumidityBit = HumidityBit + "0" # append a 0 to the humidity bitstring
                 if i>=16 and i<24: # if we're in the 3rd byte
                    TemperatureBit = TemperatureBit + "0" # append a 0 to the temperature bitstring

        except: # if there was an error in the "try:" block
           return "ERR_RANGE" # report it
           #exit(0) # end the program

        try: # do this unless there's an error. If there's an error jump to "Except:"
           for i in range(0, 8): # do this 9 times
              bit_count = 0 # reset the bit counter

              while data[count] == 0: # as long as a 0 was read
                 tmp = 1
                 count = count + 1 # move on to the next bit

              while data[count] == 1: # as long as a 1 was read
                 bit_count = bit_count + 1 # count how many 1s
                 count = count + 1 # move on to the next bit

              if bit_count > 3: # if there were at least 3 * 1-bits
                 crc = crc + "1" # add a 1 to the crc (Cyclic redundancy check) bitstring
              else: # if there were less than 3* 1-bits
                 crc = crc + "0" # add a 0 to the crc bitstring
        except: # if the "try:" block failed
           return "ERR_RANGE" # report it
           #exit(0) # end program

        Humidity = self.bin2dec(HumidityBit) # convert the binary bitstring to a decimal variable for humidity
        Temperature = self.bin2dec(TemperatureBit) # convert the binary bitstring to a decimal variable for temperature
        
        if int(Humidity) + int(Temperature) - int(self.bin2dec(crc)) == 0: # test whether the CRC indicates that the reading was good
           resultData["temp1"] = Temperature
           resultData["temp2"] = 0
           resultData["hum1"] = Humidity
           resultData["hum2"] = 0
                      
           
           if resultData["temp1"] <=0 or not isinstance(Temperature,int):
                  raise Exception("blad DHT11 temp1:" + str(resultData["temp1"]) + " hum1:"+ str(resultData["hum1"]) )
           
           
           return resultData;

        else: # if the CRC check was bad
           return "ERR_CRC" # report it


    def zapisDanych(self,data):
        
        #data = self.pobieranieDanych()
        
        sql = "insert into smash_test.temperature(temp1,temp2,hum1,hum2,iteration,sensor) values(%s,%s,%s,%s,%s,%s);"
        parameters = (data["temp1"],data["temp2"],data["hum1"],data["hum2"],data["i"],data["sensor"])
        self.da.execute(sql, parameters)