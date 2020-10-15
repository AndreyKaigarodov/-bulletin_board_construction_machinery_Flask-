from app.DBcm import UseDatabase
from config import dbconfig
from werkzeug.security import generate_password_hash, check_password_hash

class db:
    def get_by(TABLE_NAME,param, value = "null",):
        with UseDatabase(dbconfig) as cursor:
            _SQL = "select * from {} where {} = %s".format(TABLE_NAME, param)
            cursor.execute(_SQL,(value, ))
            return cursor.fetchall()

    def add_data():
        pass
    def upd_data():
        pass
    def del_data():
        pass

class User():
    TABLE_NAME = "user_customer"
    
    def __init__(self,login = None, password = None, username = None, company_name = None):
        if username != None:
            username = [x.capitalize() for x in username.lower().split()]
            self.first_name = username[0]
            self.last_name = username[1]
            self.middle_name = username[2]
            self.company_name = company_name
        self.login = login
        self.password = password
       
    def check_login_free(self):
        _SQL = "select login from {} where login = %s".format(self.TABLE_NAME)
        with UseDatabase(dbconfig) as cursor:
            cursor.execute(_SQL,(self.login,))
            data = cursor.fetchall()
            if bool(data):
                return False
        return True


    def check_login_pass(self): 
        _SQL = "select login, hash_password from {} where login =%s".format(self.TABLE_NAME)
        with UseDatabase(dbconfig) as cursor:
            cursor.execute(_SQL,(self.login,))
            data = cursor.fetchall()
            if bool(data):
                return check_password_hash(data[0]["hash_password"],self.password)
        return False
    
    def add_to_db(self):
        _SQL = """insert into {} 
                (login, hash_password, first_name, last_name, middle_name, company_name)
                values(%s, %s, %s ,%s, %s, %s)""".format(self.TABLE_NAME)
        with UseDatabase(dbconfig) as cursor:
            cursor.execute(_SQL,(self.login,generate_password_hash(self.password), self.first_name,self.last_name,
            self.middle_name, self.company_name))

    def get_by_login(self):
        user_data = db.get_by(TABLE_NAME=self.TABLE_NAME, param='login',value=self.login)
        if bool(user_data):
            return user_data[0] #возвращаем первый элемент
        return False

    def show_data(self):
        print(self.__dict__)


class UserLogin():
    def fromDB(self, user_id, db=db):
        self.__user = db.get_by(TABLE_NAME= User.TABLE_NAME, param = 'id', value= user_id)[0]
        return self
    
    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__user['id'])
    
    def get_val(self, param):
        return self.__user[param]


class UserCustomer():
    pass
       
class UserSupplier():
    pass
