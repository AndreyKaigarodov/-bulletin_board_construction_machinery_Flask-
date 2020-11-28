from flask import render_template, redirect, session
from flask.globals import request
from flask.helpers import flash, url_for
from flask_login import current_user,logout_user, login_user
from flask_login.utils import login_required

from app import app, login_manager, db
from app.forms import LoginForm, FormRegistationUser, EditProfile, FormAddTechincs
from app.modules import Technic#User,  #ТАК ТАК ТАК ТАК ТАК ТАК 
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Главная
@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')

@app.route('/list')
@login_required
def mash_list():
    
    return render_template('ListMachin.html')

#Регистрация
@app.route('/signin', methods=['GET', 'POST'])
def registrationUser():
    form = FormRegistationUser()
    if form.validate_on_submit():
        if User.query.filter_by(login = form.login.data).first() is None:
            flm = form.username.data.split()
            u = User(login=form.login.data,
                first_name = flm[0],
                last_name = flm[1],
                middle_name = flm[2],
                hash_password=generate_password_hash(form.password.data),
                company_name=form.company.data)
            db.session.add(u)
            db.session.commit()
            flash('Успешно')
            return redirect('/login')
        else:
            flash('Логин занят')
    return render_template('registrationUser.html', form = form)

#Вход 
@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(login = form.login.data).first()
        if u is not None and check_password_hash(u.hash_password, form.password.data):
            login_user(u, remember=form.remember_me.data)
            return redirect(url_for('mash_list'))
        else:
            flash('Неверный логин или пароль')
    return render_template('login.html', title = 'log in', form = form)

#Выход
@app.route('/logout', methods = ['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/<login>', methods = ['GET', 'POST'])
@login_required
def profile(login):
    if login == current_user.login:
        modalForm = EditProfile()
        if modalForm.validate_on_submit(): #Измненение профиля пользователя
            try:
                u = User.query.filter_by(login = login).first()
                #Пока только можно менять параметры ниже
                u.phone_number=modalForm.phone_number.data
                u.email = modalForm.email.data
                u.is_supplier = modalForm.start_be_supplier.data
                #позже будт обработка исключений, когда доступ к db будеет недоступен
                db.session.commit()

                flash('Успешно')
                return redirect(url_for('profile', login = current_user.login))

            except Exception as e:
                pass
        if int(current_user.is_supplier):
            modalAddTechForm = FormAddTechincs()

            #----------------------------------------
            #Пробуем выдернуть технику и засунуть в профиль пользователя
            print(User.technics)
            #----------------------------------------
            
            if  modalAddTechForm.validate_on_submit(): #добавление техники
                try:
                    technic = Technic(brand=modalAddTechForm.brand.data, model=modalAddTechForm.model.data,
                            user_id=current_user.get_val('id'), type_of_machine_id=modalAddTechForm.type_of_machine.data,
                            discription=modalAddTechForm.discription.data)
                    technic.add_to_db()
                except Exception as e:
                    print(str(e))
            return render_template('userProfile.html', form = modalForm, formTech = modalAddTechForm)
        else:
            return render_template('userProfile.html', form = modalForm, formTech = False)
        #_______________ПОДУМАЙ___________________________________
    else:
        return '<h1>{}</h1>'.format('Ошибка доступа')