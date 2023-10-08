import psycopg2
import smtplib
from email.mime.text import MIMEText
from flask import session, render_template
from Links import params_admin, params
from Admin.file_adminform import FileForm
from Authorization.cabinet import CabinetPage

from Start_page.start_page import StartPage

from Reviews.reviews import Reviews

from Events.events import Events
from Events.data import event_api

from Blog.blog import Blog

from Answers.answers import Answers

from Admin.admin import Admin
from Authorization.account import Account
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
    info = Reviews.reviews()
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        return redirect(info)


@app.route('/events/')
def open_events():
    connection = []
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
                FROM events
                ORDER BY created_date DESC; """
            )
            event_info = cursor.fetchall()
        return Events.events(event_info)
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


@app.route('/event/')
def open_event1():
    connection, mode, label = [], [], []
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
        query3 = request.args.get('mt')
        query4 = request.args.get('oa')
        query5 = request.args.get('ac')
        query6 = request.args.get('ay')
        query7 = request.args.get('ot')
        mode = ''
        label = ''
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

        if query3 and query3 != '':
            label = 'Профилактика эмоционального выгорания через муз. терапию'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_poebtmt = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = 'mt'

        elif query4 and query4 != '':
            label = '«Харизматичный оратор» 18+'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_oratory_adult = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = 'oa'

        elif query5 and query5 != '':
            label = '«Искусство общения» 12-14'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_taoc = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = 'ac'

        elif query6 and query6 != '':
            label = '«Искусство быть собой» 14-16 лет'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_taoby = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = 'ay'

        elif query7 and query7 != '':
            label = '«Харизматичный оратор» 15-18'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_oratory_teen = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = 'ot'

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")
    return Events.event(event_info, mode, label)


@app.route('/event/types/')
def open_event_type():
    page = request.args.get('page')
    if page and page != '':
        return Events.event_pages(int(page))
    return redirect('/')


@app.route('/event/buy/')
def open_buy_page():
    if session.get('authorization'):
        page = request.args.get('page')
        if page and page != '':
            try:
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                connection.autocommit = True
                with connection.cursor() as cursor:
                    cursor.execute(f'''SELECT count_of_people, id_of_people FROM events 
                                            where id = {page};''')
                    posts = cursor.fetchall()
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            item = posts[0]
            last_places = item[0] - len(item[1])
            if last_places > 0:
                return Events.event_buy_pages(int(page))
            return redirect('/')
        return redirect('/')
    else:
        return redirect('/authorization')


@app.route('/event/buy/confirm/')
def confirm():
    if session.get('authorization'):
        event = int(request.args.get('page'))
        user_id = int(session.get('id'))
        if event and event != '':
            try:
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                connection.autocommit = True
                with connection.cursor() as cursor:
                    cursor.execute(f'''SELECT count_of_people, id_of_people FROM events 
                                            where id = {event};''')
                    posts = cursor.fetchall()
            except Exception as _ex:
                print("[INFO] Error while working with PostgreSQL", _ex)
            finally:
                if connection:
                    connection.close()
                    print("[INFO] PostgreSQL connection closed")
            item = posts[0]
            last_places = item[0] - len(item[1])
            if last_places > 0:
                Events.event_confirm(event, user_id)
                return redirect(f'/event/buy/?page={int(event)}')
            return redirect('/')
        return redirect('/')
    else:
        return redirect('/authorization')


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
    info = Answers.answers()
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        return redirect(info)


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
    connection = []
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
    connection = []
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
    connection = []
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


@app.route('/email_confirm')
def email_confirm():
    email = app.config['Email_confirm'][1]
    email_code = app.config['Email_confirm'][0]

    sender = "amirhusnutdinov800900@gmail.com"
    password_email = 'smta gzvy aonh dccg'

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    template = f'''Введи меня на странице авторизации
                            {email_code} '''

    try:
        server.login(sender, password_email)
        msg = MIMEText(template, "html")
        msg["From"] = sender
        msg["To"] = email
        msg["Subject"] = "Твой код подтверждения"
        server.sendmail(sender, email, msg.as_string())

        print("The message was sent successfully!")
        return redirect('/email_confirm_page')
    except Exception as _ex:
        print(f"{_ex}\nCheck your login or password please!")
        return redirect('/')


@app.route('/email_confirm_page', methods=['GET', 'POST'])
def email_confirm_page():
    info = Account.email_confirm_page()
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        return redirect(info)
    else:
        return redirect('/')


@app.route('/reset_password')
def reset_password():
    info = Account.email_confirm_page()
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        return redirect(info)
    else:
        return redirect('/')


@app.errorhandler(404)
def page_not_found(_):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_internal_server_error(_):
    return render_template('500.html'), 500


@app.errorhandler(400)
def page_bad_request(_):
    return render_template('400.html'), 400


@app.route('/pp/')
def open_pp():
    return render_template('privacy_policy.html', title='Политика конфиденциальности персональных данных',
                           login=session.get('authorization'), **params)


app.register_blueprint(event_api.blueprint)


port = int(os.environ.get("PORT", 8080))
app.run(host='0.0.0.0', port=port)
