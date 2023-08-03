from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class BlogAdminForm(FlaskForm):
    photo_name = StringField('Photo name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    signature = TextAreaField('Answer', render_kw={"rows": 6, "cols": 11}, validators=[DataRequired()])
    text = TextAreaField('Answer', render_kw={"rows": 6, "cols": 11}, validators=[DataRequired()])
    submit = SubmitField('Отправить')
