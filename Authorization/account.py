from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from Links import about_us, blog, reviews, answers, event1, authorization, general, register


class Account:
    @staticmethod
    def account_login(method):
        if method == 'GET':
            return render_template('login.htm', general=general,
                                   about_us=about_us,
                                   blog=blog,
                                   reviews=reviews,
                                   answers=answers,
                                   event1=event1,
                                   authorization=authorization,
                                   register=register)
        elif method == 'POST':
            return [render_template('login.htm', general=general,
                                    about_us=about_us,
                                    blog=blog,
                                    reviews=reviews,
                                    answers=answers,
                                    event1=event1,
                                    authorization=authorization,
                                    register=register),
                    [request.form['email'],
                     request.form['password']]]

    @staticmethod
    def account_register(method):
        if method == 'GET':
            return render_template('registration.html', general=general,
                                   about_us=about_us,
                                   blog=blog,
                                   reviews=reviews,
                                   answers=answers,
                                   event1=event1,
                                   authorization=authorization)
        elif method == 'POST':
            print([request.form['email'],
                   request.form['password'],
                   request.form['name'],
                   request.form['surname']])
            return [render_template('registration.html', general=general,
                                    about_us=about_us,
                                    blog=blog,
                                    reviews=reviews,
                                    answers=answers,
                                    event1=event1,
                                    authorization=authorization),
                    [request.form['email'],
                     request.form['password'],
                     request.form['name'],
                     request.form['surname'],
                     request.form['photo']]]

    @staticmethod
    def users_info(blog_info: list):
        pass


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
