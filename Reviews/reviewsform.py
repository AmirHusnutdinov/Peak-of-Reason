from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ReviewsForm(FlaskForm):
    name = StringField('Email', validators=[DataRequired()])
    prof = StringField('Email', validators=[DataRequired()])
    text = TextAreaField('Answer', render_kw={"rows": 5, "cols": 11}, validators=[DataRequired()])
    submit = SubmitField('Отправить')
