from config import dbconfig
import mysql.connector
import re


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