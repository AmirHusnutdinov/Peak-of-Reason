from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BlogForm(FlaskForm):
    ids_to_delete = StringField("ids", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")
