from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired


class CabinetForm(FlaskForm):
    email = StringField('Email')
    name = StringField('Name')
    surname = StringField('Surname')
    password_old = PasswordField('Пароль')
    password_new = PasswordField('Новый пароль')
    gender = RadioField('Выберите пол', choices=[('male', 'male'), ('female', 'female')],
                        default='male', validators=[DataRequired()])
    submit = SubmitField('SAVE')
