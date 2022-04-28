from flask import Flask, render_template, redirect, abort, request
from flask_login import login_user, LoginManager, login_required, logout_user
from data import db_session
from data.users import User
from data.dishes import Dish
from forms.login import LoginForm
from forms.register import RegisterForm
from werkzeug.security import generate_password_hash
from os import remove
from PIL import Image, UnidentifiedImageError


app = Flask(__name__)
app.config['SECRET_KEY'] = 'de84.&%$djdsanj;,upy)&daogpasdnxv#&2677'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", title='Главная')


@app.route("/menu", methods=['GET'])
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
            patronymic=form.patronymic.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            number_phone=form.number_phone.data,
            age=form.age.data
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


@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html', title='Профиль')


@app.route('/account/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html', title='Настройки')


@app.route('/account/settings/add_photo/<int:id>', methods=['GET', 'POST'])
def add_photo(id):
    try:
        # request to the database
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == id).first()
        # creating variables
        name = users.email
        file = request.files['file']
        file = bytes(file.read())
        if file == b'':
            raise UnidentifiedImageError
        link_for_150px = f'static/img/users/150px/{name}.jpg'
        link_for_30px = f'static/img/users/30px/{name}.jpg'
        # recording the original
        with open(link_for_150px, 'wb') as img_150px:
            img_150px.write(file)
        with open(link_for_30px, 'wb') as img_30px:
            img_30px.write(file)
        # we change the original to the desired size
        icon_old_150px = Image.open(link_for_150px)
        icon_new_150px = icon_old_150px.resize((150, 150))
        icon_new_150px.save(link_for_150px)
        icon_old_30px = Image.open(link_for_30px)
        icon_new_30px = icon_old_30px.resize((30, 30))
        icon_new_30px.save(link_for_30px)
        # completing and saving changes
        users.icon = True
        db_sess.commit()
    except UnidentifiedImageError:
        # if the image in the form is not present
        return redirect('/account/settings')
    return redirect('/account/settings')


@app.route('/account/settings/delete_photo/<int:id>', methods=['GET', 'POST', 'DELETE'])
def delete_photo(id):
    try:
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == id).first()
        name = users.email
        remove(f'static/img/users/150px/{name}.jpg')
        remove(f'static/img/users/30px/{name}.jpg')
        users.icon = False
        db_sess.commit()
    except FileNotFoundError:
        # if there was no image at all
        return redirect('/account/settings')
    return redirect('/account/settings')


@app.route('/account/settings/update_fio/<int:id>', methods=['GET', 'POST'])
def update_fio(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    user.name = request.form.get('name')
    user.surname = request.form.get('surname')
    user.patronymic = request.form.get('patronymic')
    db_sess.commit()
    return redirect('/account/settings')


@app.route('/account/settings/update_personal/<int:id>', methods=['GET', 'POST'])
def update_personal(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    user.age = request.form.get('age')
    user.number_phone = request.form.get('number_phone')
    user.email = request.form.get('email')
    db_sess.commit()
    return redirect('/account/settings')


@app.route('/account/settings/update_password/<int:id>', methods=['GET', 'POST'])
def update_password(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    user.password = generate_password_hash(request.form.get('password'))
    db_sess.commit()
    return redirect('/account/settings')


@app.route('/account/settings/account_delete/<int:id>', methods=['GET', 'POST', 'DELETE'])
def account_delete(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == id).first()
    name = users.email
    if users:
        try:
            remove(f'static/img/users/150px/{name}.jpg')
            remove(f'static/img/users/30px/{name}.jpg')
        except FileNotFoundError:
            pass
        db_sess.delete(users)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
