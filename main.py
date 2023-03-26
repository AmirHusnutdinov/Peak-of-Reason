from flask import Flask, request

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
    all_posts = db_sess.query(Post)
    post_info = []
    for i in all_posts:
        post_info.append([i.id, i.photo_name,
                          i.name, i.signature,
                          i.link, i.created_date])
    Blog.blogs_info(post_info)
    return Blog.blog()


@app.route('/authorization')
def open_authorization():
    return Account.account()


@app.route('/answers')
def open_answers():
    return Answers.answers()


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
        db_sess2 = db_session.create_session()
        db_sess2.add(post)
        db_sess2.commit()
        return info[0]


@app.route('/about_us')
def open_about_us():
    return About.about()


app.run(port=8080, host='127.0.0.1')
