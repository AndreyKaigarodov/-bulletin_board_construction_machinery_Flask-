from config import dbconfig
import mysql.connector
import re

class db:
    def get_by(TABLE_NAME,param, value = "null",):
        with UseDatabase(dbconfig) as cursor:
            _SQL = "select * from {} where {} = %s".format(TABLE_NAME, param)
            cursor.execute(_SQL,(value, ))
            return cursor.fetchall()

    def add_data():
        pass
    def upd_data(TABLE_NAME,new_val,search_param):
        __SQL = "update {} set {} where {} = %s".format(TABLE_NAME, new_val ,search_param)
        pass
    def del_data():
        pass

class UseDatabase:
    def __init__(self, dbconfig) -> None:
        self.dbconfig = dbconfig


    def __enter__(self):
        self.conn = mysql.connector.connect(**self.dbconfig)
        self.cursor = self.conn.cursor(dictionary=True)
        return self.cursor


    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()