

from flask_login import UserMixin
from app import db
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(45), unique = True, nullable = False)
    hash_password = db.Column(db.String(200), nullable = False)   
    first_name = db.Column(db.String(45),  nullable = False)
    last_name = db.Column(db.String(45),  nullable = False)
    middle_name = db.Column(db.String(45),  nullable = False)
    phone_number = db.Column(db.String(12), nullable=True)
    company_name = db.Column(db.String(45), nullable=True)
    email = db.Column(db.String(45), nullable=True)
    image = db.Column(db.String(100), default = "baseProfile.jpg")
    is_supplier = db.Column(db.Boolean, default = 0)

    posts = db.relationship('Post', backref = 'user', lazy='dynamic')
    #technics = db.relationship('Technics')

    def __repr__(self):
        return '<User {}>'.format(self.login)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    price = db.Column(db.Integer, nullable = False)
    type_of_job = db.Column(db.String(45), nullable = False)
    discription = db.Column(db.String(100), nullable = True)
    measure_price = db.Column(db.String(45), nullable = False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    technics_id = db.Column(db.Integer, db.ForeignKey('technics.id') )

class Technics():
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(45), nullable = False)
    model = db.Column(db.String(45), nullable = False)
    discription = db.Column(db.String(45), nullable = False)
    image = db.Column(db.String(100), default = "baseTechics.png")

    posts = db.relationship('Post', backref = 'technics', lazy='dynamic')
    
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type_of_mashin_id = db.Column(db.Integer, db.ForeignKey('type_of_mashin.id'))

    

class type_of_mashin():
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    type = db.Column(db.String(45))
    technics = db.relationship('Technics', backref = 'type_of_mashin', lazy=True)

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
        return self.__user
    
    def get_val(self, param):
        return self.__user[param]