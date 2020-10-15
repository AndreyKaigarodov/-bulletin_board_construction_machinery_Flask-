from dataclasses import field
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SelectField, DateField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Length, Email, DataRequired, Regexp, ValidationError

type_of_machine = [(1, 'Погрузчик'), (2, 'Кран')]

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], description='login')
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомни меня')
    submit = SubmitField('Вход')


class FormRegistrationTechnics(FlaskForm):
    type_technics = SelectField('Тип оборудования',validators=[DataRequired()], choices = type_of_machine)
    brand_technics = StringField('Марка', validators=[DataRequired()])
    model_technics = StringField('Модель', validators=[DataRequired()])
    add_submit = SubmitField('Добавить')
    next_submit = SubmitField('Готово') 


class FormRegistationUser(FlaskForm):
    company = StringField('Компания',validators=[Length(min=0, max = 50),Regexp(r"[а-яА-яa-zA-Z\s]", message= "reg alert")])
    username = StringField('ФИО', validators=[InputRequired(), Length(min=5, max = 50),Regexp(r"[а-яА-яa-zA-Z\s]", message= "reg alert"), ])
    login = StringField('Логин', validators=[InputRequired(), Length(min=3, max = 20),Regexp(r"[a-zA-Z0-9._-]", message= "Login has invalid char")])
    password = PasswordField('Пароль', validators=[DataRequired(),Length(min=8, max = 50),EqualTo("confirm_password", message="Passwords must match")])
    confirm_password = PasswordField('Повторите пароль', validators=[EqualTo("password", message="Passwords must match")])
    #phone_number = StringField('Номер телефона')
    submit = SubmitField('Далее')
    
    def validate_username(form, field):
        if len(field.data.split()) != 3:
            raise ValidationError('Wrong username format')
    