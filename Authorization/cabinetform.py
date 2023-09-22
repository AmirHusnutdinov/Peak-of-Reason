from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FileField, DateField
from wtforms.validators import DataRequired


class CabinetForm(FlaskForm):
    email = StringField('Электронная почта')
    name = StringField('Имя')
    surname = StringField('Фамилия')
    password_old = PasswordField('Пароль')
    password_new = PasswordField('Новый пароль')
    gender = RadioField('Выберите пол', choices=[('male', 'мужчина'), ('female', 'женщина')],
                        default='male', validators=[DataRequired()])
    date_birth = DateField('Дата рождения', validators=[DataRequired()], format='%d-%m-%Y')
    fileName = FileField('Выберите фото')
    submit = SubmitField('Сохранить')
