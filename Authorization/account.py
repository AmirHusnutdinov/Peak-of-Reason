import os
import re
from database_query import database_query
from random import randint
from Authorization.email_confirmform import EmailConfirmForm
from flask import render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from Authorization.loginform import LoginForm
from Authorization.registerform import RegisterForm
from Links import params, register
from random import randrange
from settings import app, ALLOWED_EXTENSIONS


def password_check(passwd):
    special_sym = ["$", "@", "#", "%", "!", "_"]

    if len(passwd) < 8:
        return "length should be at least 8!"

    elif not any(char.isdigit() for char in passwd):
        return "Password should have at least one numeral!"

    elif not any(char.isupper() for char in passwd):
        return "Password should have at least one uppercase letter!"

    elif not any(char.islower() for char in passwd):
        return "Password should have at least one lowercase letter!"

    elif not any(char in special_sym for char in passwd):
        return "Password should have at least one of the symbols $,@,#,!,_,%"
    else:
        return passwd


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_email(email):
    if re.fullmatch(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
        return True
    return False


class Account:
    @staticmethod
    def account_login():
        connection = []
        form = LoginForm()
        if form.validate_on_submit():
            is_user = bool(database_query( f"""SELECT COUNT(*) FROM users WHERE email = '{form.email.data}';""")[0])
            if is_user:
                password_account = database_query(f"""SELECT password FROM users WHERE email = '{form.email.data}';""")[0]
                id_account = database_query( f"""SELECT user_id FROM users WHERE email = '{form.email.data}';""")[0]
                is_admin_account = database_query( f"""SELECT is_admin FROM users WHERE email = '{form.email.data}';""")[0]
            if not is_user:
                flash("Такого пользователя не существует")
                return "/authorization"
            if check_password_hash(password_account, form.password.data):
                session["authorization"] = True
                session["id"] = id_account
                if form.remember_me.data:
                    session.permanent = True
                if is_admin_account:
                    session["admin"] = True
                return "/"
            flash("Неправильный логин или пароль")
            return "/authorization"
        return render_template(
            "cabinet/login.htm",
            **params,
            register=register,
            au_is_active="active",
            form=form,
            title="Авторизация",
        )

    @staticmethod
    def account_register():
        email_cod = randint(10000, 99999)
        form = RegisterForm()
        if form.validate_on_submit():
            is_user = bool(database_query(f"""SELECT COUNT(*) FROM users WHERE email = '{form.email.data}';""")[0])
            if form.password1.data != form.password2.data:
                flash("Пароли не совпадают")
                return "/register"
            if password_check(form.password1.data) != form.password1.data:
                flash(password_check(form.password1.data))
                return "/register"
            if is_user:
                flash("Такой пользователь уже есть")
                return "/register"
            if not check_email(form.email.data):
                flash("Email не прошел проверку!")
                return "/register"
            if form.name.data.strip() == "" or form.surname.data.strip() == "":
                flash("Укажите имя и фамилию")
                return "/register"
            if len(form.name.data.strip()) <= 1 or len(form.surname.data.strip()) <= 1:
                flash("Имя и фамилия не может состоять из одного символа")
                return "/register"
            flag = False
            filename = None
            if (
                form.fileName.data.filename
                and allowed_file(form.fileName.data.filename)
                and form.fileName.data.filename != ""
            ):
                last_file = os.listdir(app.config["UPLOAD_FOLDER1"])
                last_file.sort(key=lambda x: int(os.path.splitext(x)[0]))
                last_file = last_file[-1]
                image_data = request.files[form.fileName.name].read()
                filename = (
                    str(int(last_file.split(".")[0]) + 1)
                    + "."
                    + form.fileName.data.filename.split(".")[1]
                )
                open(os.path.join(app.config["UPLOAD_FOLDER1"], filename), "wb").write(
                    image_data
                )
                flag = True
            if flag:
                photo = f"clients/{filename}"
            else:
                photo = f'clients_example/{str(randrange(1, 9)) + ".jpg"}'

            app.config["Email_confirm"] = (email_cod, form.email.data)
            database_query(f"""INSERT INTO users (name, surname, email, password, is_admin, gender, photo_way, date_birth)
                            values
                            ('{form.name.data}', '{form.surname.data}', '{form.email.data}',
                            '{generate_password_hash(form.password1.data)}', 'False'::bool,
                            '{form.gender.data}', '{photo}', '{form.date_birth.data}'::date);""")
            return "/email_confirm"
        return render_template(
            "cabinet/registration.html",
            **params,
            au_is_active="active",
            form=form,
            title="Регистрация",
        )

    @staticmethod
    def email_confirm_page():
        connection = []
        form = EmailConfirmForm()

        if form.validate_on_submit():
            user_code = form.email.data
            valid_code = app.config["Email_confirm"][0]
            email_of_user = app.config["Email_confirm"][1]

            if int(user_code) == int(valid_code):
                database_query( f"""UPDATE users
                                SET activated = 'true'
                                WHERE email = '{email_of_user}';""")
                return "/authorization"
            else:
                flash("Пароли не совпадают")
                return "/email_confirm_page"
        else:
            return render_template(
                "email/email_confirm_page.html", **params, form=form, title="Подтверждение")
