from data import db_session
from data.dishes import Dish
import os
import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
import datetime
import sqlalchemy
from sqlalchemy import orm


SqlAlchemyBase = dec.declarative_base()
__factory = None


def main():
    db_session.global_init('db/database.db')
    db_sess = db_session.create_session()
    dishes = db_sess.query(Dish)
    file = open('time.csv', 'r', encoding='utf8').read().strip().split('\n')
    print(len(file))
    file = open('time.csv', 'w', encoding='utf8')
    for dish in dishes:
        id = dish.id
        name = dish.name
        content = dish.content
        photo = dish.photo
        type = dish.type
        price = dish.price
        number_of_grams = dish.number_of_grams
        created_date = dish.created_date
        print(f'{id};{name};{content};{photo};{type};{price};{number_of_grams};{created_date}', file=file)


    # 8 полей
    # 89 блюд

if __name__ == '__main__':
    main()