from flask import Flask, render_template, redirect, make_response, request, \
    session, abort, jsonify, url_for
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from forms.login import LoginForm
from forms.register import RegisterForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'de84.&%$djdsanj;,upy)&daogpasdnxv#&2677'


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html", title='Главная')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    #if form.validate_on_submit():
    #    if form.password.data != form.password_again.data:
    #        return render_template('register.html', title='Registration',
     #                              form=form,
     #                              message="Passwords don't match")
     #   db_sess = db_session.create_session()
    #    if db_sess.query(User).filter(User.email == form.email.data).first():
    #        return render_template('register.html', title='Registration',
     #                              form=form,
     #                              message="There is already such a user")
     #   user = User(
     #       email=form.email.data,
     #       name=form.name.data,
     #       surname=form.address.data,
      #  )
      #  user.set_password(form.password.data)
     #   db_sess.add(user)
     #   db_sess.commit()
     #   return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


def main():
    app.run()


if __name__ == '__main__':
    main()