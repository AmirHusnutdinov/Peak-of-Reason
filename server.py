import os
from random import randrange

from flask import request, redirect, session

from Authorization.cabinet import CabinetPage
from Authorization.data import db_session_accaunt
from Authorization.data.users import Users
from Authorization.account import Account

from Start_page.start_page import StartPage

from Reviews.reviews import Reviews
from Reviews.data.rev import Feedback
from Reviews.data import db_session_rev

from Events.events import Events
from Events.data.teen_events import Teen_events
from Events.data.adult_events import Adult_events
from Events.data.all_events import All_events
from Events.data import db_session_event, event_api

from Blog.blog import Blog
from Blog.data import db_session_blog, blog_api
from Blog.data.Post import Post

from Answers.answers import Answers
from Answers.data import db_session_answers, answer_api
from Answers.data.answer_db import Answer_db

from Admin.admin import Admin
from Admin.data import db_session_admin
from Admin.data.admin_rev import Feedback_Admin

from About_us.about_us import About

from settings import app


@app.route('/')
def open_main():
    return StartPage.main()


@app.route('/reviews', methods=['GET', 'POST'])
def open_reviews():
    if session.get('authorization'):
        db_session_rev.global_init("Reviews/db/feedback.db")
        db_sess = db_session_rev.create_session()
        all_rev = db_sess.query(Feedback)
        rev_info = []
        for rev in all_rev:
            rev_info.append([rev.name,
                             rev.estimation,
                             rev.comment,
                             rev.created_date,
                             rev.photo])
        ind = set()
        rand_list = []
        while len(ind) != 4:
            ind.add(randrange(0, len(rev_info)))
        for i in ind:
            rand_list.append(rev_info[i])
        info = Reviews.reviews(request.method, rand_list)
        if request.method == 'GET':
            return info

        elif request.method == 'POST':
            db_session_accaunt.global_init('Authorization/db/users.db')
            dbs = db_session_accaunt.create_session()
            photo = None
            for i in dbs.query(Users):
                if i.id == session.get('id'):
                    photo = i.photo
                    
            db_session_admin.global_init("Admin/db/feedback_to_moderate.db")
            review = Feedback_Admin()
            review.name = info[0]
            review.estimation = info[1]
            review.comment = info[2]
            review.created_date = info[3]
            review.photo = photo

            db_sess = db_session_admin.create_session()
            db_sess.add(review)
            db_sess.commit()

            return redirect('/reviews')
    else:
        return redirect('/authorization')


@app.route('/events/')
def open_events():
    db_session_event.global_init("Events/db/activities.db")
    db_sess_all = db_session_event.create_session()
    all_events = db_sess_all.query(All_events)
    event_info = []
    page = request.args.get('page')
    file = None
    if page and page != '':
        file = 'event_example.html'
    for item in all_events:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.events(event_info, file)


@app.route('/event/')
def open_event1():
    db_session_event.global_init("Events/db/activities.db")
    db_sess = db_session_event.create_session()

    query1 = request.args.get('teen')
    query2 = request.args.get('adult')
    mode = ''
    all_event = []

    if query1 and query1 != '':
        all_event = db_sess.query(Teen_events)
        mode = 'teen'

    elif query2 and query2 != '':
        all_event = db_sess.query(Adult_events)
        mode = 'adult'

    event_info = []
    for item in all_event:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.event(event_info, mode)


@app.route('/event/types/')
def open_event_type():
    db_session_event.global_init("Events/db/activities.db")
    db_sess = db_session_event.create_session()
    all_event1 = db_sess.query(Teen_events)
    all_event2 = db_sess.query(Adult_events)
    event_info = []

    query1 = request.args.get('pb')
    query2 = request.args.get('tt')
    query3 = request.args.get('orator')
    query4 = request.args.get('tp')
    query5 = request.args.get('ic')
    query6 = request.args.get('ac')
    page = request.args.get('page')

    if query1 and query1 != '':
        label = 'Копилка возможностей'
        for item in all_event1:
            if item.a_piggy_bank_of_possibilities == 1:
                event_info.append([item.id,
                                   item.photo_name,
                                   item.name,
                                   item.signature,
                                   item.link,
                                   item.created_date])
        return Events.types_of_events(event_info, label)

    elif query2 and query2 != '':
        label = 'Подростковые тренинги'
        for item in all_event1:
            if item.trainings_for_teenagers == 1:
                event_info.append([item.id,
                                   item.photo_name,
                                   item.name,
                                   item.signature,
                                   item.link,
                                   item.created_date])
        return Events.types_of_events(event_info, label)

    elif query3 and query3 != '':
        label = 'Ораторское искусство'
        for item in all_event1:
            if item.oratory == 1:
                event_info.append([item.id,
                                   item.photo_name,
                                   item.name,
                                   item.signature,
                                   item.link,
                                   item.created_date])
        return Events.types_of_events(event_info, label)

    elif query4 and query4 != '':
        label = 'Тренинги для родителей'
        for item in all_event2:
            if item.trainings_for_parents == 1:
                event_info.append([item.id,
                                   item.photo_name,
                                   item.name,
                                   item.signature,
                                   item.link,
                                   item.created_date])
        return Events.types_of_events(event_info, label)

    elif query5 and query5 != '':
        label = 'Индивидуальные консультации'
        for item in all_event2:
            if item.individual_consultations == 1:
                event_info.append([item.id,
                                   item.photo_name,
                                   item.name,
                                   item.signature,
                                   item.link,
                                   item.created_date])
        return Events.types_of_events(event_info, label)

    elif query6 and query6 != '':
        label = 'Искусство общения'
        for item in all_event2:
            if item.the_art_of_communication == 1:
                event_info.append([item.id,
                                   item.photo_name,
                                   item.name,
                                   item.signature,
                                   item.link,
                                   item.created_date])
        return Events.types_of_events(event_info, label)

    elif page and page != '':
        pass

    return redirect('/')


@app.route('/blog/')
def open_blog():
    db_session_blog.global_init("Blog/db/resources.db")
    db_sess = db_session_blog.create_session()
    all_posts = db_sess.query(Post)
    posts_info = []
    for posts in all_posts:
        posts_info.append([posts.id, posts.photo_name,
                           posts.name, posts.signature,
                           posts.link, posts.created_date, posts.post_text])
    query = request.args.get('page')
    print(posts_info)
    if query and query != '':
        item = posts_info[int(query) - 1]
        print(item)
        return Blog.blog_pages(item)
    return Blog.blog(posts_info)


@app.route('/authorization', methods=['GET', 'POST'])
def open_authorization():
    if not session.get('authorization'):
        info = Account.account_login(request.method)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def open_register():
    if not session.get('authorization'):
        info = Account.account_register(request.method)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/')


@app.route('/cabinet', methods=['GET', 'POST'])
def open_cabinet():
    if session.get('authorization'):
        info = CabinetPage.account_cabinet(request.method)
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


@app.route('/cabinet/delete')
def open_cabinet_delete():
    if session.get('authorization'):
        db_sess_cabinet_del = db_session_accaunt.create_session()
        all_information_cabinet = db_sess_cabinet_del.query(Users)
        for i in all_information_cabinet:
            if i.id == session.get('id'):
                id_user = session.get('id')
                delete_id = db_sess_cabinet_del.query(Users).filter(Users.id == int(id_user)).first()
                db_sess_cabinet_del.delete(delete_id)
                db_sess_cabinet_del.commit()
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
        info = Answers.answers(request.method)

        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            db_session_answers.global_init("Answers/db/asks.db")
            answers = Answer_db()
            answers.email = info[0]
            answers.name = info[1]
            answers.answer = info[2]

            db_sess = db_session_answers.create_session()
            db_sess.add(answers)
            db_sess.commit()

            return redirect('/answers')
    else:
        return redirect('/authorization')


@app.route('/blog_admin', methods=['POST', 'GET'])
def open_admin():
    if session.get('admin'):
        info = Admin.admin(request.method)
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


UPLOAD_FOLDER = 'static/assets/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        info = Admin.event_admin(request.method)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            return redirect(info)
    else:
        return redirect('/')


db_session_accaunt.global_init("Authorization/db/users.db")
db_session_blog.global_init("Blog/db/resources.db")
db_session_answers.global_init('Answers/db/asks.db')
db_session_blog.global_init('Events/db/activities.db')
app.register_blueprint(event_api.blueprint)
app.register_blueprint(answer_api.blueprint)
app.register_blueprint(blog_api.blueprint)
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
