import psycopg2
from flask import render_template, request

from Admin.blog_adminform import BlogAdminForm
from Admin.event_adminform import EventAdminForm
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

from settings import host, user, password, db_name


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
                        ids = [0]
                with connection.cursor() as cursor:
                    cursor.execute('''SELECT to_char(current_date, 'dd-mm-yyyy');''')
                    date = cursor.fetchone()
                    date = date[0]
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""INSERT INTO blog VALUES
                                ({ids[-1]}, '{form.name.data}', '{form.signature.data}', '{form.text.data}',
                                '/blog/?page={ids[-1]}', '{date}'::date, '{form.photo_name.data}');"""
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

        all_rev = db_sess_admin.query(Feedback_Admin)
        rev_info = []
        for rev in all_rev:
            rev_info.append([rev.id,
                             rev.name,
                             rev.estimation,
                             rev.comment,
                             rev.created_date,
                             rev.photo])
        len_rev = len(rev_info)
        if method == 'GET':
            return render_template('rev_admin_page.html',
                                   **params_admin,
                                   review=rev_info,
                                   remained=len_rev, re_is='active')
        elif method == 'POST':
            for id2 in (request.form['inp1']).split():
                for item in rev_info:
                    if int(item[0]) == int(id2):
                        for i in db_sess_admin.query(Feedback_Admin):
                            if int(i.id) == int(id2):
                                db_sess_admin.delete(i)
                                db_sess_admin.commit()

            for id1 in (request.form['inp2']).split():
                for item in rev_info:
                    if int(item[0]) == int(id1):
                        rev = Feedback()
                        rev.name = item[1]
                        rev.estimation = item[2]
                        rev.comment = item[3]
                        rev.created_date = item[4]
                        rev.photo = item[5]
                        db_sess_rev.add(rev)
                        db_sess_rev.commit()

                        for i in db_sess_admin.query(Feedback_Admin):
                            if int(i.id) == int(id1):
                                db_sess_admin.delete(i)
                                db_sess_admin.commit()

            return '/reviews_admin'

    @staticmethod
    def add_photo(method, app):
        if method == 'GET':
            return render_template('add_new_image.html',
                                   **params_admin, ph_is='active')

        elif method == 'POST':
            if 'file' not in request.files:
                return request.url
            file = request.files['file']
            if file.filename == '':
                return request.url
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return '/add_photo_admin'

    @staticmethod
    def event_admin():
        form = EventAdminForm()
        if form.validate_on_submit():

            db_session_event.global_init("Events/db/activities.db")
            db_sess = db_session_event.create_session()
            all_posts = db_sess.query(All_events)
            ids = []
            for i in all_posts:
                ids.append(i.id)

            all_event = All_events()
            all_event.photo_name = form.photo_name.data
            all_event.name = form.name.data
            all_event.signature = form.signature.data
            all_event.link = f'/events/?page={(ids[-1] + 1)}'
            all_event.created_date = form.date.data

            db_sess.add(all_event)
            db_sess.commit()

            if form.category.data in ['Копилка возможностей', 'Тренинги для подростков', 'Ораторское искусство']:
                teev_event = Teen_events()
                teev_event.photo_name = form.photo_name.data
                teev_event.name = form.name.data
                teev_event.signature = form.signature.data

                if form.category.data == 'Копилка возможностей':
                    teev_event.link = all_event.link = f'/event/types/?page={(ids[-1] + 1)}pb=1'

                elif form.category.data == 'Тренинги для подростков':
                    teev_event.link = all_event.link = f'/event/types/?page={(ids[-1] + 1)}tt=1'

                elif form.category.data == 'Ораторское искусство':
                    teev_event.link = all_event.link = f'/event/types/?page={(ids[-1] + 1)}orator=1'

                teev_event.created_date = form.date.data

                if form.category.data == 'Копилка возможностей':
                    teev_event.a_piggy_bank_of_possibilities = True

                elif form.category.data == 'Тренинги для подростков':
                    teev_event.trainings_for_teenagers = True

                elif form.category.data == 'Ораторское искусство':
                    teev_event.oratory = True

                db_sess.add(teev_event)
                db_sess.commit()

                return '/event_admin'

            elif form.category.data in ['Тренинги для родителей', 'Индивидуальные консультации', 'Искусство общения']:
                adult_event = Adult_events
                adult_event.photo_name = form.photo_name.data
                adult_event.name = form.name.data
                adult_event.signature = form.signature.data

                if form.category.data == 'Тренинги для родителей':
                    adult_event.link = all_event.link = f'/event/types/?page={(ids[-1] + 1)}tp=1'

                elif form.category.data == 'Индивидуальные консультации':
                    adult_event.link = all_event.link = f'/event/types/?page={(ids[-1] + 1)}ic=1'

                elif form.category.data == 'Искусство общения':
                    adult_event.link = all_event.link = f'/event/types/?page={(ids[-1] + 1)}ac=1'

                adult_event.created_date = form.date.data

                if form.category.data == 'Тренинги для родителей':
                    adult_event.trainings_for_parents = True

                elif form.category.data == 'Индивидуальные консультации':
                    adult_event.individual_consultations = True

                elif form.category.data == 'Искусство общения':
                    adult_event.the_art_of_communication = True

                db_sess.add(adult_event)
                db_sess.commit()

                return '/event_admin'

        return render_template('admin_event.html',
                               **params_admin, ev_is='active',
                               form=form
                               )


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
