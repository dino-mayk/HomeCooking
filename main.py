from flask import Flask, render_template, redirect, abort, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from data.dishes import Dish
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.confirmation import ConfirmationForm
from werkzeug.security import generate_password_hash
from os import remove, listdir
from PIL import Image, UnidentifiedImageError
import bot, sqlalchemy.exc
from functions import *


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
            data[dish.type] = [(dish.name, dish.content, dish.photo, dish.price,
                                dish.number_of_grams, dish.created_date)]
        else:
            data[dish.type].append((dish.name, dish.content, dish.photo, dish.price,
                                    dish.number_of_grams, dish.created_date))
    db_sess.close()
    return render_template("menu.html", title='Меню', dishes=data)


@app.route("/menu/add_product/<dish>", methods=['GET'])
def add_product(dish):
    try:
        # database search and processing
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        basket = user.basket
        if basket is None:
            basket = ''
        # update data
        if basket != '':
            basket_dishes = basket.split(';')
        else:
            basket_dishes = []
        if dish not in basket_dishes:
            basket_dishes.append(dish)
        if len(basket_dishes) != 1:
            user.basket = ';'.join(basket_dishes)
        else:
            user.basket = basket_dishes[0]
        db_sess.commit()
        db_sess.close()
        return redirect('/menu')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route("/menu/delete_product/<dish>", methods=['GET'])
def delete_product_from_menu(dish):
    try:
        delete_dish(current_user.id, dish)
        return redirect('/menu')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route("/buy/delete_product/<dish>", methods=['GET'])
def delete_product_from_buy(dish):
    try:
        delete_dish(current_user.id, dish)
        return redirect('/buy')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route("/buy", methods=['GET'])
def buy():
    try:
        db_sess = db_session.create_session()
        basket = db_sess.query(User).filter(User.id == current_user.id).first().basket.split(';')
        dishes = db_sess.query(Dish).filter(Dish.name.in_(basket))
        total_price = sum([dish.price for dish in dishes])
        return render_template("buy.html", title='Заказать', dishes=dishes, total_price=total_price)
    except AttributeError:
        return redirect('/login')


@app.route("/buy/send", methods=['GET', 'POST'])
def send():
    try:
        # requesting user data
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        name = user.name
        surname = user.surname
        patronymic = user.patronymic
        email = user.email
        number_phone = user.number_phone
        age = user.age
        icon = user.icon
        if icon == 1:
            icon = f'static/img/users/150px/{email}.jpg'
        else:
            icon = ''
        # collecting data to send to the bot
        basket = db_sess.query(User).filter(User.id == current_user.id).first().basket.split(';')
        # sending data to the bot
        bot.send_telegram(f'{surname} {name} {patronymic}\n{email} {number_phone} {age}\nзаказ на {";".join(basket)}',
                          icon)
        db_sess.close()
        return redirect('/buy')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route("/gallery", methods=['GET'])
def gallery():
    photos = listdir('static/img/templates/other')
    return render_template("gallery.html", title='Наше кафе', photos=photos)


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
                                   message="Такая электронная почта уже есть")
        if db_sess.query(User).filter(User.number_phone == form.number_phone.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой номер телефона уже есть")
        global user
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            patronymic=form.patronymic.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            number_phone=form.number_phone.data,
            user_type=0,
            icon=0,
            basket='',
            age=form.age.data
        )
        return redirect('/confirmation')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    global user
    form = ConfirmationForm()
    if form.validate_on_submit():
        if form.code.data != user.control_line:
            return render_template('confirmation.html', title='Подтверждение',
                                   form=form,
                                   message="Введён неверный код подтверждения")
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    user.send_email(user.email)
    print(user.control_line)
    return render_template('confirmation.html', title='Регистрация', form=form)


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
        db_sess.close()
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
    try:
        if current_user.id:
            return render_template('account.html', title='Профиль')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route('/account/settings', methods=['GET', 'POST'])
def settings():
    try:
        if current_user.id:
            return render_template('settings.html', title='Настройки')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route('/account/settings/add_photo', methods=['GET', 'POST'])
def add_photo():
    try:
        # request to the database
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == current_user.id).first()
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
        db_sess.close()
        return redirect('/account/settings')
    except UnidentifiedImageError:
        # if the image in the form is not present
        return redirect('/account/settings')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route('/account/settings/delete_photo', methods=['GET', 'POST'])
def delete_photo():
    try:
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == current_user.id).first()
        name = users.email
        remove(f'static/img/users/150px/{name}.jpg')
        remove(f'static/img/users/30px/{name}.jpg')
        users.icon = False
        db_sess.commit()
        db_sess.close()
        return redirect('/account/settings')
    except FileNotFoundError:
        # if there was no image at all
        return redirect('/account/settings')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route('/account/settings/update_fio', methods=['GET', 'POST'])
def update_fio():
    try:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.name = request.form.get('name')
        user.surname = request.form.get('surname')
        user.patronymic = request.form.get('patronymic')
        db_sess.commit()
        db_sess.close()
        return redirect('/account/settings')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')
    except sqlalchemy.exc.IntegrityError:
        # if a registered user tries to change through a request
        return redirect('/account/settings')


@app.route('/account/settings/update_personal', methods=['GET', 'POST'])
def update_personal():
    try:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.age = request.form.get('age')
        user.number_phone = request.form.get('number_phone')
        user.email = request.form.get('email')
        db_sess.commit()
        db_sess.close()
        return redirect('/account/settings')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')
    except sqlalchemy.exc.IntegrityError:
        # if a registered user tries to change through a request
        return redirect('/account/settings')


@app.route('/account/settings/update_password', methods=['GET', 'POST'])
def update_password():
    try:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        try:
            user.password = generate_password_hash(request.form.get('password'))
            db_sess.commit()
            db_sess.close()
        except AttributeError:
            # if a registered user tries to change through a request
            return redirect('/account/settings')
        return redirect('/account/settings')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


@app.route('/account/settings/account_delete', methods=['GET', 'POST'])
def account_delete():
    try:
        db_sess = db_session.create_session()
        users = db_sess.query(User).filter(User.id == current_user.id).first()
        name = users.email
        if users:
            try:
                remove(f'static/img/users/150px/{name}.jpg')
                remove(f'static/img/users/30px/{name}.jpg')
            except FileNotFoundError:
                pass
            db_sess.delete(users)
            db_sess.commit()
            db_sess.close()
        else:
            abort(404)
        return redirect('/')
    except AttributeError:
        # if the request comes from an unregistered user
        return redirect('/login')


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()