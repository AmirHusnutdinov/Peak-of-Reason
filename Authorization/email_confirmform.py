from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EmailConfirmForm(FlaskForm):
    email = StringField("Код подтверждения", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")
