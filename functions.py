from data import db_session
from data.users import User


def delete_dish(id, product):
    # database search and processing
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    basket = user.basket
    if basket is None:
        basket = ''
    # update data
    basket_dishes = [(dish.split('_')[0], dish.split('_')[-1]) for dish in basket.split(';')]
    dict_basket_dishes = {}
    for dish in basket_dishes:
        name = dish[0]
        count = dish[-1]
        dict_basket_dishes[name] = count
    # modification and completion
    dict_basket_dishes.pop(product)
    user.basket = ';'.join([f'{dish[0]}_{dish[-1]}' for dish in dict_basket_dishes.items()])
    db_sess.commit()
    db_sess.close()