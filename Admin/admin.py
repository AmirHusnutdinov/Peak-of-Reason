import psycopg2
from flask import render_template
from Admin.blog_adminform import BlogAdminForm
from Admin.event_adminform import EventAdminForm
from Links import params_admin
import os
from settings import host, user, password, db_name, UPLOAD_FOLDER


class Admin:
    @staticmethod
    def admin():
        form = BlogAdminForm()
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
                        """SELECT id FROM blog;"""
                    )
                    ids = cursor.fetchall()
                    if not ids:
                        ids = [[0]]
                with connection.cursor() as cursor:
                    cursor.execute('''SELECT to_char(current_date, 'dd-mm-yyyy');''')
                    date = cursor.fetchone()
                    date = date[0]
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""INSERT INTO blog (id, name, signature, post_text, link, created_date, photo_way) VALUES
                                ('{int(ids[-1][0]) + 1}', '{form.name.data}', '{form.signature.data}', '{form.text.data}',
                                '/blog/?page={int(ids[-1][0]) + 1}', '{date}'::date, '{form.photo_name.data}');"""
                    )

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            return '/blog_admin'

        items = os.listdir('static/assets/images/blog')
        return render_template('admin_page.html',
                               **params_admin, bl_is='active', form=form, items=items,
                               title='Блог Админ панель'
                               )

    @staticmethod
    def admin_answers(method):
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
                    f"""SELECT id, users.email, users.name, answer FROM answers
                    INNER JOIN users ON answers.user_id = users.user_id;"""
                )
                answers_info = cursor.fetchall()

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        len_ans = len(answers_info)
        if method == 'GET':
            return render_template('admin_answers_page.html',
                                   **params_admin, remained=len_ans,
                                   answers=answers_info, an_is='active',
                                   title='Вопросы Админ панель'
                                   )

    @staticmethod
    def admin_rev(method):
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
                    f"""SELECT id, users.name, estimation, comment, to_char(created_date, 'dd-mm-yyyy'), users.user_id, 
                    users.photo_way 
                    FROM feedback_to_moderate
                    INNER JOIN users ON feedback_to_moderate.user_id = users.user_id
                    ORDER BY id ASC ;"""
                )
                rev_info = cursor.fetchall()

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")

        len_rev = len(rev_info)
        if method == 'GET':
            return render_template('rev_admin_page.html',
                                   **params_admin,
                                   review=rev_info,
                                   remained=len_rev, re_is='active', directory=UPLOAD_FOLDER,
                                   title='Отзывы Админ панель')

    @staticmethod
    def event_admin():
        form = EventAdminForm()
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
                        """SELECT id FROM events ORDER BY id DESC;"""
                    )
                    ids = cursor.fetchone()
                    if not ids:
                        ids = [1]

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            adult, teen, music, ic, taoc, oratory_teen, yourself, communicate = False, False, False, False, False, False, False, False
            if form.category.data in ["Харизматичный оратор", "Искусство быть собой", "Искусство общения"]:
                teen = True
                if form.category.data == "Харизматичный оратор":
                    link = f'/event/types/?page={(ids[0] + 1)}&ot=1'
                    oratory_teen = True

                elif form.category.data == "Искусство быть собой":
                    link = f'/event/types/?page={(ids[0] + 1)}&ay=1'
                    yourself = True

                elif form.category.data == "Искусство общения":
                    link = f'/event/types/?page={(ids[0] + 1)}&ac=1'
                    communicate = True

            elif form.category.data in ['Музыкальная терапия', 'Харизматичный оратор 18+']:
                adult = True
                if form.category.data == 'Музыкальная терапия':
                    link = f'/event/types/?page={(ids[0] + 1)}&mt=1'
                    music = True

                elif form.category.data == 'Харизматичный оратор 18+':
                    link = f'/event/types/?page={(ids[0] + 1)}&oa=1'
                    ic = True

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
                        """SELECT id FROM events;"""
                    )
                    ids = cursor.fetchall()
                    if not ids:
                        ids = [[0]]

                with connection.cursor() as cursor:
                    cursor.execute(f"""
                    insert into events 
                    (id, name, signature, created_date, link, photo_way,
                     is_teen, is_oratory_teen, is_taoby, is_taoc, 
                     is_adult, is_poebtmt, is_oratory_adult,
                    time, post_text, count_of_people, price)
                     values ('{int(ids[-1][0]) + 1}', '{form.name.data}', '{form.signature.data}', '{form.date.data}', '{link}',
                      '{form.photo_name.data}', 
                      '{teen}'::bool, '{oratory_teen}'::bool, '{yourself}'::bool, '{communicate}'::bool,
                      '{adult}'::bool, '{music}'::bool, '{ic}'::bool,
                       '{str(form.time.data)}', '{form.post_text.data}', '{form.count_of_people.data}',
                        '{form.price.data}'::int) 
                        """)

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            return '/event_admin'
        items = os.listdir('static/assets/images/event')
        return render_template('admin_event.html',
                               **params_admin, ev_is='active',
                               form=form, items=items, title='События Админ панель'
                               )


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
