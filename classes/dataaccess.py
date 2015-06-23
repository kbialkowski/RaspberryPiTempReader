#! /usr/bin/python
import MySQLdb


class DataAccess(object):
    
    host = ""
    user = ""
    password = ""
    db = ""
    
    _db_connection = None
    _db_cur = None

        
    def __init__(self):
         self._db_connection =  MySQLdb.connect(self.host,self.user,self.password,self.db)
         self._db_cur = self._db_connection.cursor()  
         
    def __del__(self):
        self._db_connection.close()
        
    def execute(self,sql,params):
        
        if self._db_connection.open==0:
            self.__init__()            
           
        self._db_cur.execute(sql, params)        
        
        
    def executeQuery(self,sql,params=()):
        
        if self._db_connection ==0:    
            self.__init__()
        
        self._db_cur.execute(sql, params)
        
        result = []
        
        for row in self._db_cur:
            result.append(row)
            
        return result
        
                
    def fetchOne(self,sql,params):
        """"""
    

         
    
    
    