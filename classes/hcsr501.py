#! /usr/bin/python
from czujnik import Czujnik 
import urllib2
from classes.dataaccess import DataAccess
import datetime

class HCSR501(Czujnik):
    
    URL = "http://192.168.4.139/image/jpeg.cgi"
    da = None
    
    def __init__(self):
        self.nazwa = "HCSR501"
        self.url = ""
        
    
    def pobieranieDanych(self):
        """"""
    def zapisDanych(self):
        
        img = self.zrobZdjecie()
        
        log = "wykryto ruch " +  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
        sql = "insert into smash_test.motion_detect(log,img,insert_data) values(%s,%s,now());";
        parameters = (log,img)
        da = DataAccess()
        da.execute(sql, parameters)
    
    def zrobZdjecie(self):
        
        opener = urllib2.build_opener()
        page = opener.open(self.URL);
        img = page.read();
        return img
        