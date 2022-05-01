import datetime
from random import randrange

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import check_password_hash
import smtplib
# import os
from email.mime.text import MIMEText


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    icon = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    basket = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number_phone = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    user_type = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def recovery_password(self):
        pass

    def send_email(self):
        self.control_line = create_control_line()
        message = f'Ваш код подтверждения: {self.control_line}'
        sender = "domkuhnyavrn@gmail.com"
        password = "domk.2022"
        # password = os.getenv("EMAIL_PASSWORD")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        try:
            server.login(sender, password)
            msg = MIMEText(message)
            msg["Subject"] = "Home Cooking"
            server.sendmail(sender, sender, msg.as_string())
            return "The message was sent successfully!"
        except Exception as _ex:
            return f"{_ex}\nCheck your login or password please!"

    def check_control_line(self, line):
        return self.control_line == line


def create_control_line():
    symbols = ('1', '#', '%', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', 'q', 'w', 'e', 'r', 't', 'y',
               'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n',
               'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'L', 'K', 'J', 'H', 'G', 'F', 'D', 'S',
               'A', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '/')
    control_line = ''
    for _ in range(7):
        control_line += symbols[randrange(len(symbols))]
    return control_line
