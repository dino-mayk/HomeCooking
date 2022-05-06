from data import db_session
from data.users import User


def delete_dish(id, dish):
    # database search and processing
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    basket = user.basket
    if basket is None:
        basket = ''
    # update data
    basket_dishes = basket.split(';')
    basket_dishes.remove(dish)
    user.basket = ' '.join(basket_dishes)
    db_sess.commit()
    db_sess.close()