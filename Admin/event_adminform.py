from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
import os

a = (os.listdir('static/assets/images/event'))
lst = []
for i in a:
    lst.append((i, i))


class EventAdminForm(FlaskForm):
    category = SelectField("Test", choices=[(1, "Копилка возможностей"),
                                            (2, "Тренинги для подростков"),
                                            (3, "Ораторское искусство"),
                                            (4, "Тренинги для родителей"),
                                            (5, "Индивидуальные консультации"),
                                            (6, "Искусство общения")],
                           validators=[DataRequired()])
    photo_name = SelectField("Test", choices=lst,
                             validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    signature = TextAreaField('Answer', render_kw={"rows": 6, "cols": 11}, validators=[DataRequired()])
    submit = SubmitField('Отправить')
