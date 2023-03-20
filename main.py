from flask import Flask

from Start_page.start_page import StartPage
from Reviews.reviews import Reviews
from Events.events import Events
from Blog.blog import Blog
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


@app.route('/events')
def open_event():
    return Events.event()


@app.route('/blog')
def open_blog():
    return Blog.blog()


@app.route('/authorization')
def open_authorization():
    return Account.account()


@app.route('/answers')
def open_answers():
    return Answers.answers()


@app.route('/admin')
def open_admin():
    return Admin.admin()


@app.route('/about_us')
def open_about_us():
    return About.about()


app.run(port=8080, host='127.0.0.1')
