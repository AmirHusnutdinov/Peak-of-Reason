from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    TextAreaField,
    SelectField,
    DateField,
    TimeField,
)
from wtforms.validators import DataRequired
import os


def photo():
    a = os.listdir("static/assets/images/event")
    lst = []
    for i in a:
        lst.append((i, i))
    return lst


class EventAdminForm(FlaskForm):
    category = SelectField(
        "Test",
        choices=[
            ("Искусство общения", "Искусство общения"),
            ("Искусство быть собой", "Искусство быть собой"),
            ("Харизматичный оратор", "Харизматичный оратор"),
            ("Музыкальная терапия", "Музыкальная терапия"),
            ("Харизматичный оратор 18+", "Харизматичный оратор 18+"),
        ],
        validators=[DataRequired()],
    )
    photo_name = SelectField("Test", choices=photo(), validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    signature = TextAreaField(
        "Answer", render_kw={"rows": 6, "cols": 11}, validators=[DataRequired()]
    )
    date = DateField("Date", validators=[DataRequired()])
    time = TimeField("Time", validators=[DataRequired()])
    post_text = TextAreaField(
        "text", render_kw={"rows": 6, "cols": 11}, validators=[DataRequired()]
    )
    count_of_people = StringField("Count_of_people", validators=[DataRequired()])
    price = StringField("price", validators=[DataRequired()])
    submit = SubmitField("Отправить")
