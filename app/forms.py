
import email_validator
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import EqualTo, InputRequired, NumberRange, Length, Email, DataRequired, Regexp, ValidationError, Optional
from wtforms.fields.html5 import EmailField, IntegerField
import phonenumbers

default_type_of_machine = [(1, 'Эскаватор колесный'), (2, 'Эскаватор-погрузчик'), 
                            (3, "Бортовой автомобиль"), (4, "Эскаватор-бульдозер"), 
                            (5, "Автокран")]# потом я обязательно свяжу с БД

default_type_of_job = [(1, 'Погрузочные работы'), (2, 'Перевоз стоительной техники'), 
                            (3, "Перевоз строительных материалов"), (4, "Грузоперевозки"), 
                            (5, "Другое")]# потом я обязательно свяжу с БД

default_type_of_measure = [(1, 'Руб/час'), (2, 'Руб/сутки'), 
                            (3, "Договорная")]

default_city = [(15, 'Екатеринбург'), (2, 'Курган'), 
                            (34, "Тюмень")]


class FormAddTechincs(FlaskForm):
    brand = StringField("Марка машины");
    model =StringField("Модель");
    discription = StringField("Дополнительное описание")
    image = FileField("Выбрать фото")
    type_of_machine = SelectField("Выбрать тип машины", choices = default_type_of_machine)

class FormAddPost(FlaskForm):
    
    price = IntegerField('Цена услуги',validators=[InputRequired(), NumberRange(min=0, message="Введите число больше 0")])
    type_of_job = SelectField('Вид работ', choices = default_type_of_job,validators=[InputRequired()])
    measure_price =  SelectField('Тип оплаты', choices = default_type_of_measure,validators=[InputRequired()])
    choice_tech = SelectField('Выбор техники',validators=[Optional()])
    choice_city = SelectField('Выбор города',choices = default_city, validators=[InputRequired()])
    discription = TextAreaField("Описание", validators=[InputRequired(),Length(min=10, max = 200),
                                                        Regexp(r"[а-яА-яa-zA-Z\s]",
                                                        message= "Использовать буквы")])
    city = SelectField("Город", choices=default_city);

    
class EditProfile(FlaskForm):
    username = StringField('ФИО', validators=[InputRequired(), Length(min=5, max = 50),
                            Regexp(r"[а-яА-яa-zA-Z\s]", message= "Only letters of the alphabet") ])
    phone_number = StringField('Номер телефона (+7)')
    email = EmailField("Email", validators=[DataRequired(),Email()])
    company = StringField('Компания',validators=[Length(min=0, max = 50),Regexp(r"[а-яА-яa-zA-Z\s]",
                            message= "Only letters of the alphabet")])
    start_be_supplier = BooleanField("Cтать поставщиком")
    #picture = FileField("Фото профиля", validators=[FileAllowed(["jpg","pdf"])])
    def validate_username(form, field):
        if len(field.data.split()) != 3:
            raise ValidationError('Wrong username format')

    def validate_phone_number(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], description='login')
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомни меня')
    submit = SubmitField('Вход')
 

class FormRegistationUser(FlaskForm):
    company = StringField('Компания',validators=[Length(min=0, max = 50),
                        Regexp(r"[а-яА-яa-zA-Z\s]", message= "Only letters of the alphabet")])
    username = StringField('ФИО', validators=[InputRequired(), Length(min=5, max = 50),
                        Regexp(r"[а-яА-яa-zA-Z\s]", message= "Only letters of the alphabet"), ])
    login = StringField('Логин', validators=[InputRequired(), Length(min=3, max = 20),
                        Regexp(r"[a-zA-Z0-9._-]", message= "Login has invalid char")])
    password = PasswordField('Пароль', validators=[DataRequired(),Length(min=8, max = 50),
                        EqualTo("confirm_password", message="Passwords must match")])
    confirm_password = PasswordField('Повторите пароль', 
                        validators=[EqualTo("password", message="Passwords must match")])
    submit = SubmitField('Далее')
    
    def validate_username(form, field):
        if len(field.data.split()) != 3:
            raise ValidationError('Wrong username format')
    