from flask import Flask

from Start_page.start_page import StartPage
from Reviews.reviews import Reviews
from Events.events import Events
from Blog.blog import Blog
from Authorization.account import Account
from Answers.answers import Answers
from Admin.admin import Admin
from About_us.about_us import About

sp = StartPage()
rev = Reviews()
ev = Events()
bl = Blog()
au = Account()
an = Answers()
ad = Admin()
ab_us = About()

app = Flask(__name__)


@app.route('/')
def open_main():
    return sp.main()


@app.route('/reviews')
def open_reviews():
    return rev.reviews()


@app.route('/events')
def open_event():
    return ev.event()


@app.route('/blog')
def open_blog():
    return bl.blog()


@app.route('/authorization')
def open_authorization():
    return au.account()


@app.route('/answers')
def open_answers():
    return an.answers()


@app.route('/admin')
def open_admin():
    return ad.admin()


@app.route('/about_us')
def open_about_us():
    return ab_us.about()


app.run(port=8080, host='127.0.0.1')
