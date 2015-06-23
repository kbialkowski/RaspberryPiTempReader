#! /usr/bin/python
from abc import ABCMeta, abstractmethod

class Czujnik(object):
    __metaclass__  = ABCMeta
    
    nazwa = ""
    
    @abstractmethod
    def pobieranieDanych(self):
        """Pobieranie danych"""
        
    @abstractmethod    
    def zapisDanych(self):
        """zapisywanie Danych"""
    
    
