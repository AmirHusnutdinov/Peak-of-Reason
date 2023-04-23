from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class EventAdminForm(FlaskForm):
    category = SelectField("Test", choices=[(0, "Копилка возможностей"), (1, "Тренинги для подростков"),
                                            (2, "Ораторское искусство"), (3, "Тренинги для родителей"),
                                            (4, "Индивидуальные консультации"), (5, "Искусство общения")],
                           validators=[DataRequired()])
    photo_name = StringField('Photo name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    signature = TextAreaField('Answer', render_kw={"rows": 6, "cols": 11}, validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Отправить')
