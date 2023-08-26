from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField, BooleanField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    password1 = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    gender = RadioField('Выберите пол', choices=['мужчина', 'женщина'],
                        default='женщина', validators=[DataRequired()])
    fileName = FileField('Выберите файл')
    checkbox = BooleanField('pp')
    submit = SubmitField('Зарегистрироваться')
