from flask import Flask, request

from Authorization.data import db_session1
from Authorization.data.users import Users
from Start_page.start_page import StartPage
from Reviews.reviews import Reviews
from Events.events import Events
from Blog.blog import Blog
from Blog.data import db_session
from Blog.data.Post import Post
from Authorization.account import Account
from Answers.answers import Answers
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
    db_session.global_init("Blog/db/resources.db")
    db_sess = db_session.create_session()
    posts = db_sess.query(Post)
    post_info = []
    for posts in posts:
        post_info.append([posts.id, posts.photo_name,
                          posts.name, posts.signature,
                          posts.link, posts.created_date])
    Blog.blogs_info(post_info)
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
        db_sess3 = db_session1.create_session1()
        db_sess3.add(user)
        db_sess3.commit()

        return info[0]


@app.route('/answers', methods=['GET', 'POST'])
def open_answers():
    info = Account.account_login(request.method)
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        return info[0]
    return Answers.answers()


@app.route('/admin')
def open_admin():
    info = Admin.admin(request.method)
    if request.method == 'GET':
        return info
    elif request.method == 'POST':
        return info[0]


@app.route('/about_us')
def open_about_us():
    return About.about()


db_session1.global_init1("Authorization/db/users.db")
db_sess1 = db_session1.create_session1()
second_post = db_sess1.query(Users)
users_info = []
for i in second_post:
    users_info.append([i.id, i.name,
                      i.surname, i.email,
                      i.password, i.is_admin,
                       i.photo])
Account.users_info(users_info)
app.run(port=8080, host='127.0.0.1')
