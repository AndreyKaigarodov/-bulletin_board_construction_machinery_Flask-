from flask import render_template, redirect, session
from flask.globals import request
from flask.helpers import flash, url_for
from flask_login import current_user,logout_user, login_user
from flask_login.utils import login_required

from app import app, login_manager
from app.forms import LoginForm, FormRegistationUser, EditProfile
from app.modules import User, UserLogin


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template('base.html')

@app.route("/list")
@login_required
def mash_list():
    
    return render_template("ListMachin.html")

@app.route('/signin', methods=['GET', 'POST'])
def registrationUser():
    form = FormRegistationUser()
    if form.validate_on_submit():
        u = User(username=form.username.data,
                    login=form.login.data,
                    password=form.password.data,
                    company_name=form.company.data)
        if u.check_login_free():
            u.add_to_db()
            flash("Успешно")
            return redirect('/login')
        else:
            flash("Логин занят")
    return render_template('registrationUser.html', form = form)


@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.login.data, form.password.data)
        if user.check_login_pass(): #если login и пароль соответствуют пользователю
            user_login = UserLogin().create(user.get_by_login())
            login_user(user_login, remember=form.remember_me.data)
            return redirect(url_for('mash_list'))
        else:
            flash("Неверный логин или пароль")
    return render_template('login.html', title = "log in", form = form)

@app.route("/logout", methods = ['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile/<login>", methods = ["GET"])
@login_required
def profile(login):
    modalForm = EditProfile()
    if login == current_user.get_val('login'):
        return render_template("userProfile.html", form = modalForm)
    else:
        return "<h1>{}</h1>".format("Ошибка доступа")