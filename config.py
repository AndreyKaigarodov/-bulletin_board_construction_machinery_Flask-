import os

dbconfig  = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'19982012',
    'database': 'find_build_techdb',
}
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY1') or 'qweqeqweqe'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://build_tech:19982012@localhost/find_build_techdb"
    
#///////