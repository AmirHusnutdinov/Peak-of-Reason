import psycopg2
from flask import render_template, request

from Admin.blog_adminform import BlogAdminForm
from Admin.event_adminform import EventAdminForm
from Admin.file_adminform import FileForm
from Links import params_admin
import os
from werkzeug.utils import secure_filename
from Events.data.teen_events import Teen_events
from Events.data.adult_events import Adult_events
from Events.data.all_events import All_events
from Events.data import db_session_event

from Reviews.data import db_session_rev
from Reviews.data.rev import Feedback

from Admin.data import db_session_admin
from Admin.data.admin_rev import Feedback_Admin

from Answers.data import db_session_answers
from Answers.data.answer_db import Answer_db

from settings import host, user, password, db_name, UPLOAD_FOLDER


class Admin:
    @staticmethod
    def admin():
        form = BlogAdminForm()
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

                # the cursor for perfoming database operations
                # cursor = connection.cursor()

                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT version();"
                    )

                    print(f"Server version: {cursor.fetchone()}")

                # get data from a table
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
                        f"""INSERT INTO blog (name, signature, post_text, link, created_date, photo_way) VALUES
                                ('{form.name.data}', '{form.signature.data}', '{form.text.data}',
                                '/blog/?page={int(ids[0][0]) + 1}', '{date}'::date, '{form.photo_name.data}');"""
                    )

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    # cursor.close()
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            return '/blog_admin'
        return render_template('admin_page.html',
                               **params_admin, bl_is='active', form=form
                               )

    @staticmethod
    def admin_answers(method):
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
                    f"""SELECT id, users.email, users.name, answer FROM answers
                    INNER JOIN users ON answers.user_id = users.user_id;"""
                )
                answers_info = cursor.fetchall()

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                # cursor.close()
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        len_ans = len(answers_info)
        if method == 'GET':
            return render_template('admin_answers_page.html',
                                   **params_admin, remained=len_ans,
                                   answers = answers_info
                                   )
        elif method == 'POST':
            delete_id = list(map(int, ''.join(request.form['inp1']).split()))
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

                # get data from a table
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""DELETE FROM answers WHERE id = {int(delete_id[0])}::int;"""
                    )

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    # cursor.close()
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            return '/answers_admin'

    @staticmethod
    def admin_rev(method):
        db_session_admin.global_init("Admin/db/feedback_to_moderate.db")
        db_session_rev.global_init("Reviews/db/feedback.db")

        db_sess_admin = db_session_admin.create_session()
        db_sess_rev = db_session_rev.create_session()
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
                    f"""SELECT id, users.name, estimation, comment, created_date, users.user_id, users.photo_way 
                    FROM feedback_to_moderate
                    INNER JOIN users ON feedback_to_moderate.user_id = users.user_id
                    ORDER BY id ASC ;"""
                )
                rev_info = cursor.fetchall()

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                # cursor.close()
                connection.close()
                print("[INFO] PostgreSQL connection closed")

        len_rev = len(rev_info)
        if method == 'GET':
            return render_template('rev_admin_page.html',
                                   **params_admin,
                                   review=rev_info,
                                   remained=len_rev, re_is='active', directory=UPLOAD_FOLDER)
        elif method == 'POST':
            for id2 in (request.form['inp1']).split():
                for item in rev_info:
                    if int(item[0]) == int(id2):
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

                            # get data from a table
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    f"""DELETE FROM feedback_to_moderate WHERE id = {int(id2)}::int;"""
                                )

                        except Exception as _ex:
                            print("[INFO] Error while working with PostgreSQL", _ex)
                        finally:
                            if connection:
                                # cursor.close()
                                connection.close()
                                print("[INFO] PostgreSQL connection closed")

            for id1 in (request.form['inp2']).split():
                for item in rev_info:
                    if int(item[0]) == int(id1):
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
                                    f"""INSERT INTO feedback (user_id, estimation, comment, created_date, photo_way) 
                                        values
                                        ((SELECT user_id FROM users WHERE user_id = {item[5]}::int), '{item[2]}',
                                        '{item[3]}', '{item[4]}'::date, 
                                        (SELECT photo_way FROM users WHERE user_id = {item[5]}::int));"""
                                )

                            with connection.cursor() as cursor:
                                cursor.execute(
                                    f"""DELETE FROM feedback_to_moderate WHERE id = {id1}::int"""
                                )

                        except Exception as _ex:
                            print("[INFO] Error while working with PostgreSQL", _ex)
                        finally:
                            if connection:
                                # cursor.close()
                                connection.close()
                                print("[INFO] PostgreSQL connection closed")

            return '/reviews_admin'

    @staticmethod
    def add_photo(method, app):
        form = FileForm()
        if form.validate_on_submit():
            print(os.listdir(app.config['UPLOAD_FOLDER1']))
            last_file = os.listdir(app.config['UPLOAD_FOLDER1'])[-1]
            image_data = request.files[form.fileName.name].read()
            filename = str(int(last_file.split('.')[0]) + 1) + '.' + form.fileName.data.filename.split('.')[1]
            open(os.path.join(app.config['UPLOAD_FOLDER1'], filename), 'wb').write(image_data)
            return '/add_photo_admin'
        return render_template('add_new_image.html',
                               **params_admin, ph_is='active', form=form)

    @staticmethod
    def event_admin():
        form = EventAdminForm()
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

                # the cursor for perfoming database operations
                # cursor = connection.cursor()

                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT version();"
                    )

                    print(f"Server version: {cursor.fetchone()}")

                # get data from a table
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT id FROM events ORDER BY id DESC;"""
                    )
                    ids = cursor.fetchone()
                    if not ids:
                        ids = [1]
                with connection.cursor() as cursor:
                    cursor.execute('''SELECT to_char(current_date, 'dd-mm-yyyy');''')
                    date = cursor.fetchone()[0]

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    # cursor.close()
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            adult, teen, tfp, ic, taoc, apbop, tft, oratory = False, False, False, False, False, False, False, False

            if form.category.data in ['Копилка возможностей', 'Тренинги для подростков', 'Ораторское искусство']:
                teen = True
                if form.category.data == 'Копилка возможностей':
                    link = f'/event/types/?page={(ids[0] + 1)}pb=1'
                    apbop = True

                elif form.category.data == 'Тренинги для подростков':
                    link = f'/event/types/?page={(ids[0] + 1)}tt=1'
                    tft = True

                elif form.category.data == 'Ораторское искусство':
                    link = f'/event/types/?page={(ids[0] + 1)}orator=1'
                    oratory = True

            elif form.category.data in ['Тренинги для родителей', 'Индивидуальные консультации', 'Искусство общения']:
                adult = True
                if form.category.data == 'Тренинги для родителей':
                    link = f'/event/types/?page={(ids[0] + 1)}tp=1'
                    tfp = True

                elif form.category.data == 'Индивидуальные консультации':
                    link = f'/event/types/?page={(ids[0] + 1)}ic=1'
                    ic = True

                elif form.category.data == 'Искусство общения':
                    link = f'/event/types/?page={(ids[0] + 1)}ac=1'
                    taoc = True
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

                # get data from a table
                with connection.cursor() as cursor:
                    cursor.execute(f'''insert into events 
                    (name, signature, created_date, link, photo_way, is_teen, is_apbop, is_tft, is_oratory, is_adult,
                    is_tfp, is_ic, is_taoc)
                     values ('{form.name.data}', '{form.signature.data}', '{date}'::date, '{link}',
                      '{form.photo_name.data}', 
                      '{teen}'::bool, '{apbop}'::bool, '{tft}'::bool, '{oratory}'::bool,
                      '{adult}'::bool, '{tfp}'::bool, '{ic}'::bool, '{taoc}'::bool);''')

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    # cursor.close()
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            return '/event_admin'

        return render_template('admin_event.html',
                               **params_admin, ev_is='active',
                               form=form
                               )


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
