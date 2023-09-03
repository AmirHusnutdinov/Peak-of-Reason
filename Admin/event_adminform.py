from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
import os

a = (os.listdir('static/assets/images/event'))
lst = []
for i in a:
    lst.append((i, i))


class EventAdminForm(FlaskForm):
    category = SelectField("Test", choices=[("Копилка возможностей", "Копилка возможностей"),
                                            ("Тренинги для подростков", "Тренинги для подростков"),
                                            ("Ораторское искусство", "Ораторское искусство"),
                                            ("Тренинги для родителей", "Тренинги для родителей"),
                                            ("Индивидуальные консультации", "Индивидуальные консультации"),
                                            ("Искусство общения", "Искусство общения")],
                           validators=[DataRequired()])
    photo_name = SelectField("Test", choices=lst,
                             validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    signature = TextAreaField('Answer', render_kw={"rows": 6, "cols": 11}, validators=[DataRequired()])
    submit = SubmitField('Отправить')
