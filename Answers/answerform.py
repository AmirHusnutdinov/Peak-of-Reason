from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AnswerForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    text = TextAreaField('Answer', render_kw={"rows": 10, "cols": 11}, validators=[DataRequired()])
    submit = SubmitField('PUSH')
