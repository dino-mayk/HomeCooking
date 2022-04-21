from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager, login_required, logout_user
from data import db_session
from data.users import User
from data.dishes import Dish
from forms.login import LoginForm
from forms.register import RegisterForm
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = 'de84.&%$djdsanj;,upy)&daogpasdnxv#&2677'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html", title='Главная')


@app.route("/menu", methods=['GET', 'POST'])
def menu():
    db_sess = db_session.create_session()
    dishes = db_sess.query(Dish)
    data = {}
    for dish in dishes:
        if dish.type not in data:
            data[dish.type] = [(dish.name, dish.content, dish.photo, dish.created_date)]
        else:
            data[dish.type].append((dish.name, dish.content, dish.photo, dish.created_date))
    return render_template("menu.html", title='Меню', dishes=data)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html', title='Настройки')


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
