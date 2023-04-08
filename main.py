import datetime
from flask import flash
from random import randrange
import os

from flask import Flask, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash

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
from Events.data import db_session_event

from Blog.blog import Blog
from Blog.data import db_session_blog
from Blog.data.Post import Post

from Answers.answers import Answers
from Answers.data import db_session_answers
from Answers.data.answer_db import Answer_db

from Admin.admin import Admin
from Admin.data import db_session_admin
from Admin.data.admin_rev import Feedback_Admin

from About_us.about_us import About

app = Flask(__name__)
app.config['SECRET_KEY'] = '__secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)


@app.route('/')
def open_main():
    return StartPage.main()


def password_check(passwd):
    special_sym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 8:
        val = False
        return 'length should be at least 8'

    if not any(char.isdigit() for char in passwd):
        val = False
        return 'Password should have at least one numeral'

    if not any(char.isupper() for char in passwd):
        val = False
        return 'Password should have at least one uppercase letter'

    if not any(char.islower() for char in passwd):
        val = False
        return 'Password should have at least one lowercase letter'

    if not any(char in special_sym for char in passwd):
        val = False
        return 'Password should have at least one of the symbols $,@,#'
    if val:
        return val


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


@app.route('/events')
def open_events():
    db_session_event.global_init("Events/db/activities.db")
    db_sess_all = db_session_event.create_session()
    all_events = db_sess_all.query(All_events)
    event_info = []
    for item in all_events:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.events(event_info)


@app.route('/event1/')
def open_event1():
    db_session_event.global_init("Events/db/activities.db")
    db_sess = db_session_event.create_session()
    all_event1 = db_sess.query(Teen_events)
    event_info = []
    for item in all_event1:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.event1(event_info)


@app.route('/event2/')
def open_event2():
    db_session_event.global_init("Events/db/activities.db")
    db_sess = db_session_event.create_session()
    all_event2 = db_sess.query(Adult_events)
    event_info = []
    for item in all_event2:
        event_info.append([item.id,
                           item.photo_name,
                           item.name,
                           item.signature,
                           item.link,
                           item.created_date])
    return Events.event2(event_info)


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
    if not session.get('authorization'):
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
    return redirect('/')


app.config['UPLOAD_FOLDER1'] = 'static/assets/images/clients'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/register', methods=['GET', 'POST'])
def open_register():
    if not session.get('authorization'):
        info = Account.account_register(request.method)

        if request.method == 'GET':
            return info

        elif request.method == 'POST':
            if info[1] != info[2]:
                flash('Пароли не совпадают')
                return Account.account_register('GET')
            print(password_check(info[1]), info[1])
            if password_check(info[1]) != info[1]:
                flash(password_check(info[1]))
                return Account.account_register('GET')
            db_sess = db_session_accaunt.create_session()

            if db_sess.query(Users).filter(Users.email == info[0]).first():
                flash("Такой пользователь уже есть")
                return Account.account_register('GET')
            if info[3].strip() == '' or info[4].strip() == '':
                flash("Укажите имя и фамилию")
                return Account.account_register('GET')
            if len(info[3].strip()) <= 1 or len(info[4].strip()) <= 1:
                flash("Имя и фамилия не может состоять из одного символа")
                return Account.account_register('GET')

            if 'file' not in request.files:
                flash('Не могу прочитать файл')
                return redirect(request.url)
            file = request.files['file']
            flag = False
            filename = None
            if file and allowed_file(file.filename) and file.filename != '':
                filename = str(int(os.listdir('static/assets/images/clients')[-1].split('.')[0]) + 1) + '.jpg'
                file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
                flag = True
            one_user = Users()
            one_user.email = info[0]
            one_user.password = generate_password_hash(info[1])
            one_user.name = info[3].strip()
            one_user.surname = info[4].strip()
            one_user.gender = info[5]
            if flag:
                one_user.photo = f'clients/{filename}'
            else:
                one_user.photo = f'clients_example/{str(randrange(1, 10)) + ".jpg"}'
            db_sess.add(one_user)
            db_sess.commit()

            return redirect('/authorization')
    else:
        return redirect('/')


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
                flash('Это не ваш старый пароль')
                return CabinetPage.account_cabinet('GET', em, na, sur, gen)
            if users.email != change_data_user[0] and change_data_user[0] != '':
                if db_sess_cabinet.query(Users).filter(Users.email == change_data_user[0]).first():
                    flash("Такой пользователь с такой почтой уже зарегистрирован")
                    return CabinetPage.account_cabinet('GET', em, na, sur, gen)
                else:
                    users.email = change_data_user[0]
            if users.name != change_data_user[1] and change_data_user[1].strip() != '':
                if change_data_user[1].strip() == '':
                    flash("Укажите имя")
                    return CabinetPage.account_cabinet('GET', em, na, sur, gen)
                elif len(change_data_user[1].strip()) <= 1:
                    flash("Имя не может состоять из одного символа")
                    return CabinetPage.account_cabinet('GET', em, na, sur, gen)
                else:
                    users.name = change_data_user[1]
            if users.surname != change_data_user[2] and change_data_user[2].strip() != '':
                if change_data_user[2].strip() == '':
                    flash("Укажите фамилию")
                    return CabinetPage.account_cabinet('GET', em, na, sur, gen)
                elif len(change_data_user[2].strip()) <= 1:
                    flash("Фамилия не может состоять из одного символа")
                    return CabinetPage.account_cabinet('GET', em, na, sur, gen)
                else:
                    users.surname = change_data_user[2]
            if change_data_user[4].strip() != '' and change_data_user[3].strip() != '':
                if password_check(change_data_user[4]) != change_data_user[4]:
                    flash(password_check(change_data_user[4]))
                    return CabinetPage.account_cabinet('GET', em, na, sur, gen)
                else:
                    users.password = generate_password_hash(change_data_user[4])
            if users.gender != change_data_user[5]:
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
        db_sess_cabinet_del = db_session_accaunt.create_session()
        all_information_cabinet = db_sess_cabinet_del.query(Users)
        for i in all_information_cabinet:
            if i.id == session.get('id'):
                inditification = session.get('id')
                delete_id = db_sess_cabinet_del.query(Users).filter(Users.id == int(inditification)).first()
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

app.run(port=8080, host='127.0.0.1')
