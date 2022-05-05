from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class ConfirmationForm(FlaskForm):
    code = StringField('Код подтверждения', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')