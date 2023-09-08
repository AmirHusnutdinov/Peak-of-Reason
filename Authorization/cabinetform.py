from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField
from wtforms.validators import DataRequired


class CabinetForm(FlaskForm):
    email = StringField('Электронная почта')
    name = StringField('Имя')
    surname = StringField('Фамилия')
    password_old = PasswordField('Пароль')
    password_new = PasswordField('Новый пароль')
    gender = RadioField('Выберите пол', choices=[('male', 'мужчина'), ('female', 'женщина')],
                        default='male', validators=[DataRequired()])
    fileName = FileField('Выберите фото')
    submit = SubmitField('Сохранить')
