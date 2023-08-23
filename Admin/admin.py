import psycopg2
from flask import render_template
from Admin.blog_adminform import BlogAdminForm
from Admin.event_adminform import EventAdminForm
from Links import params_admin

from settings import host, user, password, db_name, UPLOAD_FOLDER


class Admin:
    @staticmethod
    def admin():
        form = BlogAdminForm()
        print(form.photo_name)
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
                        f"""INSERT INTO blog (name, signature, post_text, link, created_date, photo_way) VALUES
                                ('{form.name.data}', '{form.signature.data}', '{form.text.data}',
                                '/blog/?page={int(ids[0][0]) + 1}', '{date}'::date, '{form.photo_name.data}');"""
                    )

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")

            return '/blog_admin'
        import os
        items = os.listdir('static/assets/images/blog')
        return render_template('admin_page.html',
                               **params_admin, bl_is='active', form=form, items=items
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
                                   answers=answers_info, an_is='active'
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
                                   remained=len_rev, re_is='active', directory=UPLOAD_FOLDER)

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
                with connection.cursor() as cursor:
                    cursor.execute('''SELECT to_char(current_date, 'dd-mm-yyyy');''')
                    date = cursor.fetchone()[0]

            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
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
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                connection.autocommit = True

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
