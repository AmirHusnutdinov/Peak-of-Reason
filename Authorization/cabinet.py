import psycopg2
from flask import render_template, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from Authorization.account import password_check, check_email
from Authorization.cabinetform import CabinetForm
from Authorization.data import db_session_accaunt
from Authorization.data.users import Users
from Links import delete, params, logout
from settings import host, user, password, db_name


class CabinetPage:
    @staticmethod
    def account_cabinet():
        global gender
        db_sess_cabinet = db_session_accaunt.create_session()
        all_information_cabinet = db_sess_cabinet.query(Users)
        gender = ''
        email = ''
        name = ''
        surname = ''
        form = CabinetForm()
        try:
            # connect to exist database
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            # the cursor for perfoming database operations
            # cursor = connection.cursor()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT version();"
                )

                print(f"Server version: {cursor.fetchone()}")

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT email, name, surname, password, gender, photo_way 
                    FROM users
                    WHERE user_id = '{session.get("id")}'::int;"""
                )
                user_list = cursor.fetchall()[0]
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                # cursor.close()
                connection.close()
                print("[INFO] PostgreSQL connection closed")

        if form.validate_on_submit():
            try:
                # connect to exist database
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                connection.autocommit = True
                if form.password_old.data.strip() == '':
                    flash('Чтобы изменить данные введите пароль')
                    return '/cabinet'
                if not check_password_hash(user_list[3], form.password_old.data) and form.password_old.data.strip() != '':
                    flash('Это не ваш старый пароль')
                    return '/cabinet'
                if user_list[0] != form.email.data and form.email.data.strip() != '':
                    if db_sess_cabinet.query(Users).filter(Users.email == form.email.data).first():
                        flash("Такой пользователь с такой почтой уже зарегистрирован")
                        return '/cabinet'
                    else:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""UPDATE users
                                SET email = '{form.email.data}'
                                WHERE user_id = '{session.get("id")}'::int;"""
                            )
                if not check_email(form.email.data.strip()) and form.email.data.strip() != '':
                    flash("Email не прошел проверку!")
                    return '/cabinet'
                if user_list[1] != form.name.data and form.name.data.strip() != '':
                    if form.name.data.strip() == '':
                        flash("Укажите имя")
                        return '/cabinet'
                    elif len(form.name.data.strip()) <= 1:
                        flash("Имя не может состоять из одного символа")
                        return '/cabinet'
                    else:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""UPDATE users
                                SET name = '{form.name.data}'
                                WHERE user_id = '{session.get("id")}'::int;"""
                            )
                if user_list[2] != form.surname.data and form.surname.data.strip() != '':
                    if form.surname.data.strip() == '':
                        flash("Укажите фамилию")
                        return '/cabinet'
                    elif len(form.surname.data.strip()) <= 1:
                        flash("Фамилия не может состоять из одного символа")
                        return '/cabinet'
                    else:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""UPDATE users
                                SET surname = '{form.surname.data}'
                                WHERE user_id = '{session.get("id")}'::int;"""
                            )
                if form.password_new.data.strip() != '' and form.password_old.data.strip() != '':
                    if password_check(form.password_new.data) != form.password_new.data:
                        flash(password_check(form.password_new.data))
                        return '/cabinet'
                    else:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""UPDATE users
                                SET password = '{generate_password_hash(form.password_new.data)}'
                                WHERE user_id = '{session.get("id")}'::int;"""
                            )
                if user_list[4] != form.gender.data:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""UPDATE users
                            SET gender = '{form.gender.data}'
                            WHERE user_id = '{session.get("id")}'::int;"""
                        )
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    # cursor.close()
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            return '/cabinet'

        email = user_list[0]
        name = user_list[1]
        surname = user_list[2]
        form.gender.data = user_list[4]

        return render_template('cabinet.html', **params,
                               delete=delete, logout=logout, email=email, name=name, surname=surname,
                               is_cabinet='-after', form=form,
                               title='Your cabinet')

    @staticmethod
    def account_cabinet_del():
        try:
            # connect to exist database
            connection = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
            connection.autocommit = True

            # the cursor for perfoming database operations
            # cursor = connection.cursor()

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT version();"
                )

                print(f"Server version: {cursor.fetchone()}")

            with connection.cursor() as cursor:
                cursor.execute(
                    f"""DELETE FROM users
                    WHERE user_id = '{session.get("id")}'::int;"""
                )
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                # cursor.close()
                connection.close()
                print("[INFO] PostgreSQL connection closed")
