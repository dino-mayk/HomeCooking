from flask import Flask, render_template
from waitress import serve
from data import db_session
from data.dishes import Dish
from os import listdir
import sqlalchemy.exc, json


app = Flask(__name__)
with open('security.json', 'r', encoding='utf8') as security:
    security = json.load(security)
    app.config['SECRET_KEY'] = security['flask_secret_key']


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

@app.route("/location", methods=['GET'])
def location():
    return render_template("location.html", title='Месторасположение')

@app.route("/gallery", methods=['GET'])
def gallery():
    photos = listdir('static/img/templates/')
    return render_template("gallery.html", title='Наше кафе', photos=photos)

def main():
    db_session.global_init("db/database.db")
    #serve(app, host='0.0.0.0', port=5000, url_scheme='https')
    app.run()


if __name__ == '__main__':
    main()