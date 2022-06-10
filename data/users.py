import datetime, random, sqlalchemy, smtplib, json, ssl
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    icon = sqlalchemy.Column(sqlalchemy.String, default="")
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    basket = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    number_phone = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def recovery_password(self):
        pass

    def send_email(self, recipient):
        with open('security.json', 'r', encoding='utf8') as security:
            security = json.load(security)
            sender_email = security['mail']
            password = security['mail_password']
            smtp_server = "smtp.gmail.com"
            port = 587
            self.control_line = create_control_line()
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg['To'] = recipient
            body_text = MIMEText(self.control_line, 'plain')  # 
            msg.attach(body_text)
            context = ssl.create_default_context()
            
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient, msg.as_string())
        except Exception as error:
            print(error)
        finally:
            server.quit()

    def check_control_line(self, line):
        return self.control_line == line


def create_control_line():
    return str(random.randrange(1000, 9999))