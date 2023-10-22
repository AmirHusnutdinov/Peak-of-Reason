from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField


class GeneratePageForm(FlaskForm):
    request = StringField("Введите свой запрос", validators=[DataRequired()])
    submit = SubmitField("SEND")
