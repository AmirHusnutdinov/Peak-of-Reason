import os

import psycopg2
from flask import request, redirect, session

from Authorization.cabinet import CabinetPage
from Authorization.account import Account

from Start_page.start_page import StartPage

from Reviews.reviews import Reviews
from Reviews.data import feedback_api

from Events.events import Events
from Events.data.teen_events import Teen_events
from Events.data.adult_events import Adult_events
from Events.data.all_events import All_events
from Events.data import db_session_event, event_api

from Blog.blog import Blog
from Blog.data import db_session_blog, blog_api

from Answers.answers import Answers
from Answers.data import answer_api

from Admin.admin import Admin

from About_us.about_us import About

from settings import app, host, user, password, db_name


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
        # connect to exist database
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
            # cursor.close()
            connection.close()
            print("[INFO] PostgreSQL connection closed")


@app.route('/event/')
def open_event1():
    try:
        # connect to exist database
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
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_teen = 'true'::bool;"""
                )
                event_info = cursor.fetchall()

            mode = 'teen'

        elif query2 and query2 != '':
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')   
                    FROM events WHERE is_adult = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            mode = 'adult'
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            # cursor.close()
            connection.close()
            print("[INFO] PostgreSQL connection closed")
    return Events.event(event_info, mode)


@app.route('/event/types/')
def open_event_type():
    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        query1 = request.args.get('pb')
        query2 = request.args.get('tt')
        query3 = request.args.get('orator')
        query4 = request.args.get('tp')
        query5 = request.args.get('ic')
        query6 = request.args.get('ac')
        page = request.args.get('page')

        if query1 and query1 != '':
            label = 'Копилка возможностей'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_apbop = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query2 and query2 != '':
            label = 'Подростковые тренинги'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_tft = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query3 and query3 != '':
            label = 'Ораторское искусство'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_oratory = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query4 and query4 != '':
            label = 'Тренинги для родителей'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_tfp = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query5 and query5 != '':
            label = 'Индивидуальные консультации'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_ic = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif query6 and query6 != '':
            label = 'Искусство общения'
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT id, photo_way, name, signature, link, to_char(created_date, 'dd Mon YYYY')  
                    FROM events WHERE is_taoc = 'true'::bool;"""
                )
                event_info = cursor.fetchall()
            return Events.types_of_events(event_info, label)

        elif page and page != '':
            pass
    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            # cursor.close()
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


@app.route('/about_us')
def open_about_us():
    return About.about()


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


@app.route('/add_photo_admin', methods=['GET', 'POST'])
def open_add_photo():
    if session.get('admin'):
        info = Admin.add_photo(request.method, app)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/')


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


db_session_blog.global_init("Blog/db/resources.db")

app.register_blueprint(feedback_api.blueprint)
app.register_blueprint(event_api.blueprint)
app.register_blueprint(answer_api.blueprint)
app.register_blueprint(blog_api.blueprint)

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
