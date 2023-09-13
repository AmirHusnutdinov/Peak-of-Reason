import psycopg2
from flask import session, render_template
from Links import params_admin, params
from Admin.file_adminform import FileForm
from Authorization.cabinet import CabinetPage
from Authorization.account import Account

from Start_page.start_page import StartPage

from Reviews.reviews import Reviews
from Reviews.data import feedback_api

from Events.events import Events
from Events.data import event_api

from Blog.blog import Blog
from Blog.data import db_session_blog, blog_api

from Answers.answers import Answers
from Answers.data import answer_api

from Admin.admin import Admin

from settings import app, host, user, password, db_name


import os
from flask import flash, request, redirect
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def open_main():
    return StartPage.main()


@app.route('/reviews', methods=['GET', 'POST'])
def open_reviews():
    if session.get('authorization'):
        info = Reviews.reviews()
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/authorization')


@app.route('/events/')
def open_events():
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
                f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                FROM events;"""
            )
            event_info = cursor.fetchall()
        page = request.args.get('page')
        file = None
        if page and page != '':
            file = 'event_example.html'
        return Events.events(event_info, file)
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


@app.route('/event/')
def open_event1():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        query1 = request.args.get('teen')
        query2 = request.args.get('adult')
        mode = ''

        if query1 and query1 != '':
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd MM YYYY')  
                    FROM events WHERE is_teen = 'true'::bool;"""
                )
                event_info = cursor.fetchall()

            mode = 'teen'

        elif query2 and query2 != '':
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')   
                    FROM events WHERE is_adult = 'true'::bool;"""
                               )
                event_info = cursor.fetchall()
            mode = 'adult'
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
    return Events.event(event_info, mode)


@app.route('/event/types/')
def open_event_type():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        query1 = request.args.get('mt')
        query2 = request.args.get('oa')
        query3 = request.args.get('ac')
        query4 = request.args.get('ay')
        query5 = request.args.get('ot')
        page = request.args.get('page')

        if query1 and query1 != '':
            label = 'Профилактика эмоционального выгорания через музтерапию'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_poebtmt = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query2 and query2 != '':
            label = '«Харизматичный оратор» 18+'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_oratory_adult = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query3 and query3 != '':
            label = '«Искусство общения» 12-14'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_taoc = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query4 and query4 != '':
            label = '«Искусство быть собой» 14-16 лет'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_taoby = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query5 and query5 != '':
            label = '«Харизматичный оратор» 15-18'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_oratory_teen = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif page and page != '':
            return Events.event_pages(int(page))
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
    return redirect('/')


@app.route('/blog/')
def open_blog():
    query = request.args.get('page')
    if query and query != '':
        return Blog.blog_pages(int(query))
    return Blog.blog()


@app.route('/authorization', methods=['GET', 'POST'])
def open_authorization():
    if not session.get('authorization'):
        info = Account.account_login()
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def open_register():
    if not session.get('authorization'):
        info = Account.account_register()
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/')


@app.route('/cabinet', methods=['GET', 'POST'])
def open_cabinet():
    if session.get('authorization'):
        info = CabinetPage.account_cabinet()
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/authorization')


@app.route('/cabinet/logout')
def open_cabinet_logout():
    if session.get('authorization'):
        session.permanent = False
        session.pop('authorization', None)
        session.pop('id', None)
        session.pop('admin', None)
        return redirect('/')
    else:
        return redirect('/authorization')


@app.route('/cabinet/delete', methods=['GET', 'POST'])
def open_cabinet_delete():
    if session.get('authorization'):
        if request.method == 'GET':
            CabinetPage.account_cabinet_del()
            session.permanent = False
            session.pop('authorization', None)
            session.pop('id', None)
            session.pop('admin', None)
            return redirect('/')
    else:
        return redirect('/authorization')


@app.route('/answers', methods=['GET', 'POST'])
def open_answers():
    if session.get('authorization'):
        info = Answers.answers()
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/authorization')


@app.route('/blog_admin', methods=['POST', 'GET'])
def open_admin():
    if session.get('admin'):
        info = Admin.admin()
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/')


@app.route('/answers_admin', methods=['GET', 'POST'])
def open_admin_answers():
    if session.get('admin'):
        info = Admin.admin_answers(request.method)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/')


@app.route('/reviews_admin', methods=['GET', 'POST'])
def open_reviews_admin():
    if session.get('admin'):
        info = Admin.admin_rev(request.method)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/')


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_photo_admin', methods=['GET', 'POST'])
def open_add_photo():
    form = FileForm()
    if request.method == 'GET':
        return render_template('add_new_image.html',
                               **params_admin, ph_is='active', form=form)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)

            file.save(os.path.join(f'static/assets/images/{request.form["teamDropdown"]}', filename))

            return render_template('add_new_image.html',
                                   **params_admin, ph_is='active', form=form)


@app.route('/event_admin', methods=['GET', 'POST'])
def open_event_admin():
    if session.get('admin'):
        info = Admin.event_admin()
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/')


@app.route('/add_feedback/', methods=['GET'])
def open_feedback_add():
    if session.get('admin'):
        id_to_add = request.args.get('id')
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
                feedback_to_add = ''
                rev_info = cursor.fetchall()

                # Получили все отзывы на модерацию,
                # чтобы получить нужный по ID и его в модерации удалить, а в основу добавить

                for i in rev_info:
                    if int(i[0]) == int(id_to_add):
                        feedback_to_add = i

                print(feedback_to_add)

                cursor.execute(
                    f"""Insert into feedback(user_id, estimation, comment, created_date, photo_way)
                     values({feedback_to_add[5]}, {feedback_to_add[2]},
                    '{feedback_to_add[3]}', '{feedback_to_add[4]}', '{feedback_to_add[6]}')""")

                cursor.execute(
                    f"""Delete from feedback_to_moderate where id = {id_to_add}""")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        return redirect('/reviews_admin')
    else:
        return redirect('/')


@app.route('/delete_feedback/', methods=['GET'])
def open_feedback_delete():
    if session.get('admin'):
        id_to_delete = request.args.get('id')
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
                    f"""Delete from feedback_to_moderate where id = {id_to_delete}""")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        return redirect('/reviews_admin')
    else:
        return redirect('/')


@app.route('/delete_answer/', methods=['GET'])
def open_answer_delete():
    if session.get('admin'):
        id_to_delete = request.args.get('id')
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
                    f"""Delete from answers where id = {id_to_delete}""")

        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)

        finally:
            if connection:
                connection.close()
                print("[INFO] PostgreSQL connection closed")
        return redirect('/answers_admin')
    else:
        return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(400)
def page_bad_request(e):
    return render_template('400.html'), 400


@app.route('/pp/')
def open_pp():
    return render_template('privacy_policy.html', title='Политика конфиденциальности персональных данных', login=session.get('authorization'), **params)


db_session_blog.global_init("Blog/db/resources.db")

app.register_blueprint(feedback_api.blueprint)
app.register_blueprint(event_api.blueprint)
app.register_blueprint(answer_api.blueprint)
app.register_blueprint(blog_api.blueprint)

port = int(os.environ.get("PORT", 8080))
app.run(host='0.0.0.0', port=port)
