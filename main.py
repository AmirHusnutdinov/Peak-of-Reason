import datetime
from flask import flash
from random import randrange
import os

from flask import Flask, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from Authorization.cabinet import CabinetPage
from Authorization.data import db_session_accaunt
from Authorization.data.users import Users
from Authorization.account import Account

from Start_page.start_page import StartPage

from Reviews.reviews import Reviews
from Reviews.data.rev import Feedback
from Reviews.data import db_session_rev

from Events.events import Events
from Events.data.event_file1 import Event1
from Events.data.event_file2 import Event2
from Events.data.event_file3 import Event3
from Events.data.event_file4 import Event4
from Events.data import db_session_event

from Blog.blog import Blog
from Blog.data import db_session_blog
from Blog.data.Post import Post

from Answers.answers import Answers
from Answers.data import db_session_answers
from Answers.data.answer_db import Answer_db

from Admin.admin import Admin
from Admin.data import db_session_admin
from Admin.data.admin_rev import Feedback

from About_us.about_us import About

app = Flask(__name__)
app.config['SECRET_KEY'] = '__secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)


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
            db_session_admin.global_init("Admin/db/feedback_to_moderate.db")
            review = Feedback()
            review.name = info[0]
            review.estimation = info[1]
            review.comment = info[2]
            review.created_date = info[3]

            db_sess = db_session_admin.create_session()
            db_sess.add(review)
            db_sess.commit()

            return redirect('/reviews')
    else:
        return redirect('/authorization')


@app.route('/event1')
def open_event1():
    db_session_event.global_init("Events/db/activities.db")
    db_sess = db_session_event.create_session()
    all_event1 = db_sess.query(Event1)
    event_info = []
    for item in all_event1:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.event1(event_info)


@app.route('/event2')
def open_event2():
    db_session_event.global_init("Events/db/activities.db")
    db_sess = db_session_event.create_session()
    all_event2 = db_sess.query(Event2)
    event_info = []
    for item in all_event2:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.event2(event_info)


@app.route('/event3')
def open_event3():
    db_session_event.global_init("Events/db/activities.db")
    db_sess = db_session_event.create_session()
    all_event3 = db_sess.query(Event3)
    event_info = []
    for item in all_event3:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.event3(event_info)


@app.route('/event4')
def open_event4():
    db_session_event.global_init("Events/db/activities.db")
    db_sess = db_session_event.create_session()
    all_event4 = db_sess.query(Event4)
    event_info = []
    for item in all_event4:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.event4(event_info)


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
    if query and query != '':
        item = posts_info[int(query) - 1]
        return Blog.blog_pages(item)
    return Blog.blog(posts_info)


@app.route('/authorization', methods=['GET', 'POST'])
def open_authorization():
    info = Account.account_login(request.method)
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        db_sess = db_session_accaunt.create_session()
        all_information = db_sess.query(Users)
        for i in all_information:
            if str(i.email) == info[0] and check_password_hash(i.password, info[1]):
                session['authorization'] = True
                session['id'] = i.id
                if info[2] == 'on':
                    session.permanent = True
                if i.is_admin:
                    session['admin'] = True
                return redirect('/')
        flash("Неправильный логин или пароль")
        return Account.account_login('GET')


@app.route('/register', methods=['GET', 'POST'])
def open_register():
    info = Account.account_register(request.method)
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        if info[1] != info[2]:
            flash('Пароли не совпадают')
            return Account.account_register('GET')
        db_sess = db_session_accaunt.create_session()
        if db_sess.query(Users).filter(Users.email == info[0]).first():
            flash("Такой пользователь уже есть")
            return Account.account_register('GET')
        one_user = Users()
        one_user.email = info[0]
        one_user.password = generate_password_hash(info[1])
        one_user.name = info[3]
        one_user.surname = info[4]
        one_user.gender = info[5]
        db_sess.add(one_user)
        db_sess.commit()

        return redirect('/authorization')


@app.route('/cabinet', methods=['GET', 'POST'])
def open_cabinet():
    em, na, sur, gen = '', '', '', ''
    if session.get('authorization'):
        db_sess_cabinet = db_session_accaunt.create_session()
        all_information_cabinet = db_sess_cabinet.query(Users)
        if request.method == 'GET':
            for i in all_information_cabinet:
                if i.id == session.get('id'):
                    em = i.email
                    na = i.name
                    sur = i.surname
                    gen = i.gender
            return CabinetPage.account_cabinet('GET', em, na, sur, gen)
        elif request.method == 'POST':
            change_data_user = CabinetPage.account_cabinet('POST', '', '', '', '')
            users = db_sess_cabinet.query(Users).filter(Users.id == session.get('id')).first()
            if not check_password_hash(users.password, change_data_user[3]) and change_data_user[3] != '':
                flash('Пароли не совпадают')
                return CabinetPage.account_cabinet('GET', em, na, sur, gen)
            if users.email != change_data_user[0] and change_data_user[0] != '':
                users.email = change_data_user[0]
            elif users.name != change_data_user[1] and change_data_user[1] != '' and change_data_user[1] != ' ':
                users.name = change_data_user[1]
            elif users.surname != change_data_user[2] and change_data_user[2] != '' and change_data_user[2] != ' ':
                users.surname = change_data_user[2]
            elif change_data_user[4] != '' and change_data_user[3] != '':
                users.password = generate_password_hash(change_data_user[4])
            elif users.gender != change_data_user[5]:
                users.gender = change_data_user[5]
            db_sess_cabinet.merge(users)
            db_sess_cabinet.commit()

        return redirect('/')
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
        db_sess_cabinet = db_session_accaunt.create_session()
        all_information_cabinet = db_sess_cabinet.query(Users)
        for i in all_information_cabinet:
            if i.id == session.get('id'):
                id = session.get('id')
                delete_id = db_sess_cabinet.query(Users).filter(Users.id == int(id)).first()
                db_sess_cabinet.delete(delete_id)
                db_sess_cabinet.commit()
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
            db_session_blog.global_init("Blog/db/resources.db")
            db_sess = db_session_blog.create_session()
            all_posts = db_sess.query(Post)
            ids = []
            for id_ in all_posts:
                ids.append(id_.id)
            post = Post()
            post.photo_name = info[0]
            post.name = info[1]
            post.signature = info[2]
            post.link = f'http://127.0.0.1:8080/blog/?page={(ids[-1] + 1)}'
            post.post_text = info[3]
            post.created_date = info[4]

            db_sess = db_session_blog.create_session()
            db_sess.add(post)
            db_sess.commit()

            return redirect('/blog_admin')
    else:
        return redirect('/')


@app.route('/about_us')
def open_about_us():
    return About.about()


@app.route('/answers_admin', methods=['GET', 'POST'])
def open_admin_answers():
    if session.get('admin'):
        db_session_answers.global_init("Answers/db/asks.db")
        db_sess = db_session_answers.create_session()
        all_answers = db_sess.query(Answer_db)
        answers_info = []
        for answers in all_answers:
            answers_info.append([answers.id,
                                 answers.email,
                                 answers.name,
                                 answers.answer])
        info = Admin.admin_answers(request.method, answers_info)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            delete_id = list(map(int, ''.join(info[1]).split()))
            for id_ in delete_id:
                deleted_answer = db_sess.query(Answer_db).filter(Answer_db.id == id_).first()
                db_sess.delete(deleted_answer)
                db_sess.commit()

            return redirect('/answers_admin')
    else:
        return redirect('/')


@app.route('/reviews_admin', methods=['GET', 'POST'])
def open_reviews_admin():
    if session.get('admin'):
        db_session_admin.global_init("Admin/db/feedback_to_moderate.db")
        db_session_rev.global_init("Reviews/db/feedback.db")
        db_sess_admin = db_session_admin.create_session()
        db_sess_rev = db_session_rev.create_session()
        all_rev = db_sess_admin.query(Feedback)
        rev_info = []
        for rev in all_rev:
            rev_info.append([rev.id,
                             rev.name,
                             rev.estimation,
                             rev.comment,
                             rev.created_date])
        info = Admin.admin_rev(request.method, rev_info)
        if request.method == 'GET':
            return info

        elif request.method == 'POST':
            for id2 in info[1]:
                for item in info[0]:
                    if int(item[0]) == int(id2):
                        delete_id = db_sess_admin.query(Feedback).filter(Feedback.id == int(id2)).first()
                        db_sess_admin.delete(delete_id)
                        db_sess_admin.commit()

            for id1 in info[2]:
                for item in info[0]:
                    print(int(item[0]), int(id1))
                    if int(item[0]) == int(id1):
                        rev = Feedback()
                        rev.name = item[1]
                        rev.estimation = item[2]
                        rev.comment = item[3]
                        rev.created_date = item[4]
                        db_sess_rev.add(rev)
                        db_sess_rev.commit()

                        delete_id = db_sess_admin.query(Feedback).filter(Feedback.id == int(id1)).first()
                        db_sess_admin.delete(delete_id)
                        db_sess_admin.commit()

            return redirect('/reviews_admin')
    else:
        return redirect('/')


ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
UPLOAD_FOLDER = 'static/assets/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_photo_admin', methods=['GET', 'POST'])
def open_add_photo():
    if session.get('admin'):
        info = Admin.add_photo(request.method)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            if 'file' not in request.files:
                flash('Не могу прочитать файл')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('Нет выбранного файла')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect('/add_photo_admin')
    else:
        return redirect('/')


@app.route('/event_admin', methods=['GET', 'POST'])
def open_event_admin():
    if session.get('admin'):
        info = Admin.event_admin(request.method)
        if request.method == 'GET':
            return info
        elif request.method == 'POST':
            db_session_event.global_init("Events/db/activities.db")
            db_sess = db_session_event.create_session()
            if int(info[0]) == 1:
                ev = Event1()
                ev.photo_name = info[1]
                ev.name = info[2]
                ev.signature = info[3]
                ev.link = info[4]
                ev.created_date = info[5]

                db_sess.add(ev)
                db_sess.commit()

                return redirect('/event_admin')

            elif int(info[0]) == 2:
                ev = Event2()
                ev.photo_name = info[1]
                ev.name = info[2]
                ev.signature = info[3]
                ev.link = info[4]
                ev.created_date = info[5]

                db_sess.add(ev)
                db_sess.commit()

                return redirect('/event_admin')

            elif int(info[0]) == 3:
                ev = Event3()
                ev.photo_name = info[1]
                ev.name = info[2]
                ev.signature = info[3]
                ev.link = info[4]
                ev.created_date = info[5]

                db_sess.add(ev)
                db_sess.commit()

                return redirect('/event_admin')

            elif int(info[0]) == 4:
                ev = Event4()
                ev.photo_name = info[1]
                ev.name = info[2]
                ev.signature = info[3]
                ev.link = info[4]
                ev.created_date = info[5]

                db_sess.add(ev)
                db_sess.commit()

                return redirect('/event_admin')
    else:
        return redirect('/')


db_session_accaunt.global_init("Authorization/db/users.db")

app.run(port=8080, host='127.0.0.1')
