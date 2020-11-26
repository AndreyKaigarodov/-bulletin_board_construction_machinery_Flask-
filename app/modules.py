from app.DBcm import UseDatabase, db

from config import dbconfig
from werkzeug.security import generate_password_hash, check_password_hash

class Technic():
    TABLE_NAME = "technics"

    def __init__(self, brand,model,user_id ,
                type_of_machine_id,discription="Описание отсутствует", image = "baseTechnicPhoto"):
        self.brand = brand
        self.model = model
        self.discription = discription
        self.type_of_machine_id = type_of_machine_id
        self.image = image
        self.user_id = user_id
    
    def add_to_db(self):
        _SQL = """insert into {} 
                (brand, discription, image, model, type_of_mashin_id, user_id)
                values(%s, %s, %s ,%s, %s, %s)""".format(self.TABLE_NAME) # тут надо будет переименовать type_of mashin 
        with UseDatabase(dbconfig) as cursor:
            cursor.execute(_SQL,(self.brand, self.discription,self.image,
                                self.model, self.type_of_machine_id, self.user_id,))


class User():
    TABLE_NAME = "user"
    
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

#Переделать, это для теста
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def get_mashine(self):
        _SQL = """select brand, discription, model, type_of_mashin_id from user
                    left join technics
                    on user.id = technics.user_id
                    where login = %s""" # максимально плохой запраос !!!!!!!!
        with UseDatabase(dbconfig) as cursor:
            cursor.execute(_SQL,(self.login,))
            data = cursor.fetchall()
            return data
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        

    def update_data(self,**kwargs):
        new_val = str(kwargs)[2:-1].replace(":","=").replace(" ","").replace("'=","=").replace(",'",",") #простите
        db.upd_data(self.TABLE_NAME, new_val,"login", self.login)
       

    def show_data(self):
        print(self.__dict__)





class UserCustomer():
    pass
       
class UserSupplier():
    pass
