from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, EmailField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    number_phone = StringField('Номер телефона', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    patronymic = StringField('Отчество', validators=[DataRequired()])
    age = StringField('Ваш возраст', validators=[DataRequired()])
    submit = SubmitField('Сохранить')