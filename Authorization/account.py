import os
import re
from random import randint
import smtplib
from email.mime.text import MIMEText
import psycopg2
from flask import render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from Authorization.loginform import LoginForm
from Authorization.registerform import RegisterForm
from Links import params, register
from random import randrange
from settings import app, ALLOWED_EXTENSIONS, host, user, password, db_name


def password_check(passwd):
    special_sym = ['$', '@', '#', '%', '!', '_']

    if len(passwd) < 8:
        return 'length should be at least 8!'

    elif not any(char.isdigit() for char in passwd):
        return 'Password should have at least one numeral!'

    elif not any(char.isupper() for char in passwd):
        return 'Password should have at least one uppercase letter!'

    elif not any(char.islower() for char in passwd):
        return 'Password should have at least one lowercase letter!'

    elif not any(char in special_sym for char in passwd):
        return 'Password should have at least one of the symbols $,@,#,!,_,%'
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
    def account_login():
        connection = []
        form = LoginForm()
        if form.validate_on_submit():
            try:
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                connection.autocommit = True

                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT COUNT(*) FROM users WHERE email = '{form.email.data}';"""
                    )
                    is_user = bool(cursor.fetchone()[0])
                if is_user:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""SELECT password FROM users WHERE email = '{form.email.data}';"""
                        )
                        password_account = cursor.fetchone()[0]
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""SELECT user_id FROM users WHERE email = '{form.email.data}';"""
                        )
                        id_account = cursor.fetchone()[0]
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""SELECT is_admin FROM users WHERE email = '{form.email.data}';"""
                        )
                        is_admin_account = cursor.fetchone()[0]

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            if not is_user:
                flash("Такого пользователя не существует")
                return '/authorization'
            if check_password_hash(password_account, form.password.data):
                session['authorization'] = True
                session['id'] = id_account
                if form.remember_me.data:
                    session.permanent = True
                if is_admin_account:
                    session['admin'] = True
                return '/'
            flash("Неправильный логин или пароль")
            return '/authorization'
        return render_template('login.htm', **params, register=register,
                               au_is_active='active', form=form,
                               title='Authorization')

    @staticmethod
    def account_register():
        email_cod = randint(10000, 99999)
        connection = []
        form = RegisterForm()
        if form.validate_on_submit():
            try:
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                connection.autocommit = True

                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT COUNT(*) FROM users WHERE email = '{form.email.data}';"""
                    )
                    is_user = bool(cursor.fetchone()[0])

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            if form.password1.data != form.password2.data:
                flash('Пароли не совпадают')
                return '/register'
            if password_check(form.password1.data) != form.password1.data:
                flash(password_check(form.password1.data))
                return '/register'
            if is_user:
                flash("Такой пользователь уже есть")
                return '/register'
            if not check_email(form.email.data):
                flash("Email не прошел проверку!")
                return '/register'
            if form.name.data.strip() == '' or form.surname.data.strip() == '':
                flash("Укажите имя и фамилию")
                return '/register'
            if len(form.name.data.strip()) <= 1 or len(form.surname.data.strip()) <= 1:
                flash("Имя и фамилия не может состоять из одного символа")
                return '/register'
            flag = False
            filename = None
            if form.fileName.data.filename and allowed_file(form.fileName.data.filename) and \
                    form.fileName.data.filename != '':
                last_file = os.listdir(app.config['UPLOAD_FOLDER1'])
                last_file.sort(key=lambda x: int(os.path.splitext(x)[0]))
                last_file = last_file[-1]
                image_data = request.files[form.fileName.name].read()
                filename = str(int(last_file.split('.')[0]) + 1) + '.' + form.fileName.data.filename.split('.')[1]
                open(os.path.join(app.config['UPLOAD_FOLDER1'], filename), 'wb').write(image_data)
                flag = True
            if flag:
                photo = f'clients/{filename}'
            else:
                photo = f'clients_example/{str(randrange(1, 9)) + ".jpg"}'
            try:
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                connection.autocommit = True

                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""INSERT INTO users (name, surname, email, password, is_admin, gender, photo_way, date_birth)
                            values
                            ('{form.name.data}', '{form.surname.data}', '{form.email.data}',
                            '{generate_password_hash(form.password1.data)}', 'False'::bool,
                            '{form.gender.data}', '{photo}', '{form.date_birth.data}'::date);""")

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            return '/authorization'
        return render_template('registration.html', **params,
                               au_is_active='active', form=form,
                               title='Register')
