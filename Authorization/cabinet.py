import os
from flask import render_template, session, flash, request
from werkzeug.security import check_password_hash, generate_password_hash
from Authorization.account import password_check, check_email
from Authorization.cabinetform import CabinetForm
from Links import delete, params, logout
from database_query import database_query
from settings import (
    UPLOAD_FOLDER,
    ALLOWED_EXTENSIONS,
    app,
)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class CabinetPage:
    @staticmethod
    def account_cabinet():
        global gender
        gender = ""
        form = CabinetForm()
        user_list = database_query( f"""SELECT email, name, surname, password, gender, photo_way, date_birth
                    FROM users
                    WHERE user_id = '{session.get("id")}'::int;""")[0]
        if form.validate_on_submit():
            if form.password_old.data.strip() == "":
                flash("Чтобы изменить данные введите пароль")
                return "/cabinet"
            if (not check_password_hash(user_list[3], form.password_old.data)
                and form.password_old.data.strip() != ""):
                flash("Это не ваш старый пароль")
                return "/cabinet"
            if user_list[0] != form.email.data and form.email.data.strip() != "":
                email_is_one = bool(database_query(f"""SELECT COUNT(*) FROM users
                            WHERE email = '{form.email.data.strip()}';""")[0])
                if email_is_one:
                    flash("Такой пользователь с такой почтой уже зарегистрирован")
                    return "/cabinet"
                else:
                    database_query(f"""UPDATE users
                                SET email = '{form.email.data}'
                                WHERE user_id = '{session.get("id")}'::int;""")
                if (not check_email(form.email.data.strip())
                    and form.email.data.strip() != ""
                ):
                    flash("Email не прошел проверку!")
                    return "/cabinet"
                if user_list[1] != form.name.data and form.name.data.strip() != "":
                    if form.name.data.strip() == "":
                        flash("Укажите имя")
                        return "/cabinet"
                    elif len(form.name.data.strip()) <= 1:
                        flash("Имя не может состоять из одного символа")
                        return "/cabinet"
                    else:
                        database_query(f"""UPDATE users
                                SET name = '{form.name.data}'
                                WHERE user_id = '{session.get("id")}'::int;""")
                if (
                    user_list[2] != form.surname.data
                    and form.surname.data.strip() != ""
                ):
                    if form.surname.data.strip() == "":
                        flash("Укажите фамилию")
                        return "/cabinet"
                    elif len(form.surname.data.strip()) <= 1:
                        flash("Фамилия не может состоять из одного символа")
                        return "/cabinet"
                    else:
                        database_query(f"""UPDATE users
                                SET surname = '{form.surname.data}'
                                WHERE user_id = '{session.get("id")}'::int;""")
                if (
                    form.password_new.data.strip() != ""
                    and form.password_old.data.strip() != ""
                ):
                    if password_check(form.password_new.data) != form.password_new.data:
                        flash(password_check(form.password_new.data))
                        return "/cabinet"
                    else:
                        database_query( f"""UPDATE users
                                SET password = '{generate_password_hash(form.password_new.data)}'
                                WHERE user_id = '{session.get("id")}'::int;""")
                if user_list[4] != form.gender.data:
                    database_query(f"""UPDATE users
                            SET gender = '{form.gender.data}'
                            WHERE user_id = '{session.get("id")}'::int;""")
                if (
                    form.fileName.data.filename
                    and allowed_file(form.fileName.data.filename)
                    and form.fileName.data.filename != ""
                    and form.fileName.data.filename != user_list[5]
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
                    open(
                        os.path.join(app.config["UPLOAD_FOLDER1"], filename), "wb"
                    ).write(image_data)
                    database_query(f"""UPDATE users
                            SET photo_way = '{'clients/' + filename}'
                            WHERE user_id = '{session.get("id")}'::int;""")
                if form.date_birth.data != user_list[6]:
                    database_query(f"""UPDATE users
                            SET date_birth = '{form.date_birth.data}'::date
                            WHERE user_id = '{session.get("id")}'::int;""")
            return "/cabinet"

        email = user_list[0]
        name = user_list[1]
        surname = user_list[2]
        photo_way = user_list[5]
        form.gender.data = user_list[4]
        date_birth = user_list[6]

        return render_template(
            "cabinet/cabinet.html",
            **params,
            delete=delete,
            logout=logout,
            email=email,
            name=name,
            surname=surname,
            photo_way=photo_way,
            directory=UPLOAD_FOLDER,
            is_cabinet="-after",
            form=form,
            date_birth=date_birth,
            title="Личный кабинет",
            login=session.get("authorization"),
        )

        return render_template(
            "cabinet/cabinet.html",
            **params,
            delete=delete,
            logout=logout,
            email=email,
            name=name,
            surname=surname,
            photo_way=photo_way,
            directory=UPLOAD_FOLDER,
            is_cabinet="-after",
            form=form,
            date_birth=date_birth,
            title="Your cabinet",
            login=session.get("authorization"),
        )

    @staticmethod
    def account_cabinet_del():
        database_query(f"""DELETE FROM users
                    WHERE user_id = '{session.get("id")}'::int;""")
