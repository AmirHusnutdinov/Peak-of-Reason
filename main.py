from flask import Flask, request

from Authorization.data import db_session_accaunt
from Authorization.data.users import Users
from Authorization.account import Account

from Start_page.start_page import StartPage

from Reviews.reviews import Reviews

from Events.events import Events

from Blog.blog import Blog
from Blog.data import db_session_blog
from Blog.data.Post import Post

from Answers.answers import Answers
from Answers.data import db_session_answers
from Answers.data.answer_db import Answers

from Admin.admin import Admin

from About_us.about_us import About

app = Flask(__name__)
app.config['SECRET_KEY'] = '__secret_key'


@app.route('/')
def open_main():
    return StartPage.main()


@app.route('/reviews')
def open_reviews():
    return Reviews.reviews()


@app.route('/event1')
def open_event1():
    return Events.event1()


@app.route('/event2')
def open_event2():
    return Events.event2()


@app.route('/event3')
def open_event3():
    return Events.event3()


@app.route('/event4')
def open_event4():
    return Events.event4()


@app.route('/blog')
def open_blog():
    db_session_blog.global_init("Blog/db/resources.db")
    db_sess = db_session_blog.create_session()
    all_posts = db_sess.query(Post)
    posts_info = []
    for posts in all_posts:
        posts_info.append([posts.id, posts.photo_name,
                          posts.name, posts.signature,
                          posts.link, posts.created_date])
    Blog.blogs_info(posts_info)
    return Blog.blog()


@app.route('/authorization', methods=['GET', 'POST'])
def open_authorization():
    info = Account.account_login(request.method)
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        return info[0]


@app.route('/register', methods=['GET', 'POST'])
def open_register():
    info = Account.account_register(request.method)
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        user = Users()
        user.email = info[1][0]
        user.password = info[1][1]
        user.name = info[1][2]
        user.surname = info[1][3]
        db_sess = db_session_accaunt.create_session()
        db_sess.add(user)
        db_sess.commit()

        return info[0]


@app.route('/answers', methods=['GET', 'POST'])
def open_answers():
    info = Answers.answers(request.method)
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        db_session_answers.global_init("Answers/db/asks.db")
        answers = Answers()
        answers.email = info[1][0]
        answers.name = info[1][1]
        answers.answer = info[1][2]

        db_sess = db_session_answers.create_session()
        db_sess.add(answers)
        db_sess.commit()

        return info[0]


@app.route('/admin',  methods=['POST', 'GET'])
def open_admin():
    info = Admin.admin(request.method)
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        post = Post()
        
        post.photo_name = info[1][0]
        post.name = info[1][1]
        post.signature = info[1][2]
        post.link = info[1][3]
        post.created_date = info[1][4]
        
        db_sess = db_session_blog.create_session()
        db_sess.add(post)
        db_sess.commit()
        
        return info[0]


@app.route('/about_us')
def open_about_us():
    return About.about()


db_session_accaunt.global_init("Authorization/db/users.db")
db_sess = db_session_accaunt.create_session()
users = db_sess.query(Users)
users_info = []
for user in users:
    users_info.append([user.id, user.name,
                      user.surname, user.email,
                      user.password, user.is_admin,
                       user.photo])
Account.users_info(users_info)
app.run(port=8080, host='127.0.0.1')
