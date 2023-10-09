from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
import os


def photo():
    a = os.listdir("static/assets/images/blog")
    lst = []
    for i in a:
        lst.append((i, i))
    return lst


class BlogAdminForm(FlaskForm):
    lst = photo()
    photo_name = SelectField("Test", choices=lst, validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    signature = TextAreaField(
        "Answer", render_kw={"rows": 5, "cols": 11}, validators=[DataRequired()]
    )
    text = TextAreaField(
        "Answer", render_kw={"rows": 5, "cols": 11}, validators=[DataRequired()]
    )
    submit = SubmitField("Отправить")
