from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ReviewsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    prof = StringField('Prof', validators=[DataRequired()])
    text = TextAreaField('Review', render_kw={"rows": 5, "cols": 11}, validators=[DataRequired()])
    submit = SubmitField('Отправить')
