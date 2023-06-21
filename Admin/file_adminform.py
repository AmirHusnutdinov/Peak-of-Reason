from flask_wtf import FlaskForm

from wtforms import SubmitField, FileField


class FileForm(FlaskForm):

    fileName = FileField('Выберите фото:')

    submit = SubmitField('SEND')
