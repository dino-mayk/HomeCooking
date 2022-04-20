from flask import Flask, render_template, redirect
from data import db_session
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'de84.&%$djdsanj;,upy)&daogpasdnxv#&2677'


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html", title='Главная')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
