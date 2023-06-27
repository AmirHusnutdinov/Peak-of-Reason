from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    password1 = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    gender = RadioField('Выберите пол', choices=['male', 'female'],
                        default='male', validators=[DataRequired()])
    fileName = FileField('Select file')
    submit = SubmitField('Sign in')
