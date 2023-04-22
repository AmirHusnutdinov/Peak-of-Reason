import os
import re
from random import randrange
from flask import render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from Authorization.data import db_session_accaunt
from Authorization.data.users import Users
from Links import params

from settings import app, ALLOWED_EXTENSIONS


def password_check(passwd):
    special_sym = ['$', '@', '#', '%']

    if len(passwd) < 8:
        return 'length should be at least 8!'

    elif not any(char.isdigit() for char in passwd):
        return 'Password should have at least one numeral!'

    elif not any(char.isupper() for char in passwd):
        return 'Password should have at least one uppercase letter!'

    elif not any(char.islower() for char in passwd):
        return 'Password should have at least one lowercase letter!'

    elif not any(char in special_sym for char in passwd):
        return 'Password should have at least one of the symbols $,@,#!'
    else:
        return passwd


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_email(email):
    if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
        return True
    return False


class Account:
    @staticmethod
    def account_login(method):
        if method == 'GET':
            return render_template('login.htm', **params,
                                   au_is_active='active')
        elif method == 'POST':
            if len(request.form) == 3:
                mass_login = [request.form['email'], request.form['password'], request.form['check']]
            else:
                mass_login = [request.form['email'], request.form['password'], 'off']

            db_sess = db_session_accaunt.create_session()
            all_information = db_sess.query(Users)
            for i in all_information:
                if str(i.email) == mass_login[0] and check_password_hash(i.password, mass_login[1]):
                    session['authorization'] = True
                    session['id'] = i.id
                    if mass_login[2] == 'on':
                        session.permanent = True
                    if i.is_admin:
                        session['admin'] = True
                    return '/'
            flash("Неправильный логин или пароль")
            return '/authorization'

    @staticmethod
    def account_register(method):
        if method == 'GET':
            return render_template('registration.html', **params,
                                   au_is_active='active')
        elif method == 'POST':

            mass_register = [request.form['email'],
                             request.form['password1'],
                             request.form['password2'],
                             request.form['name'],
                             request.form['surname'],
                             request.form['inlineRadioOptions']]
            db_sess = db_session_accaunt.create_session()
            if mass_register[1] != mass_register[2]:
                flash('Пароли не совпадают')
                return '/register'
            if password_check(mass_register[1]) != mass_register[1]:
                flash(password_check(mass_register[1]))
                return '/register'
            if db_sess.query(Users).filter(Users.email == mass_register[0]).first():
                flash("Такой пользователь уже есть")
                return '/register'
            if not check_email(mass_register[0]):
                flash("Email не прошел проверку!")
                return '/register'
            if mass_register[3].strip() == '' or mass_register[4].strip() == '':
                flash("Укажите имя и фамилию")
                return '/register'
            if len(mass_register[3].strip()) <= 1 or len(mass_register[4].strip()) <= 1:
                flash("Имя и фамилия не может состоять из одного символа")
                return '/register'

            if 'file' not in request.files:
                flash('Не могу прочитать файл')
                return '/register'
            file = request.files['file']
            flag = False
            filename = None
            if file and allowed_file(file.filename) and file.filename != '':
                filename = str(int(os.listdir('static/assets/images/clients')[-1].split('.')[0]) + 1) + '.jpg'
                file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
                flag = True
            one_user = Users()
            one_user.email = mass_register[0]
            one_user.password = generate_password_hash(mass_register[1])
            one_user.name = mass_register[3].strip()
            one_user.surname = mass_register[4].strip()
            one_user.gender = mass_register[5]
            if flag:
                one_user.photo = f'clients/{filename}'
            else:
                one_user.photo = f'clients_example/{str(randrange(1, 10)) + ".jpg"}'
            db_sess.add(one_user)
            db_sess.commit()

            return '/authorization'

    @staticmethod
    def users_info(blog_info: list):
        pass
