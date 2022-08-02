from flask import jsonify, Blueprint, abort

from utils import get_one_user, get_all_users, get_all_orders, get_one_order, get_all_offers, get_one_offer

movie_blueprint = Blueprint("movie_blueprint", __name__)


@movie_blueprint.route("/users")
def get_all_users_views():
    return jsonify(get_all_users())


@movie_blueprint.route("/users/<int:user_id>")
def get_one_user_views(user_id):
    try:
        return jsonify(get_one_user(user_id))
    except AttributeError:
        return abort(404, ValueError("No such user found|Такой пользователь не найден"))


@movie_blueprint.route("/orders")
def get_all_orders_views():
    return jsonify(get_all_orders())


@movie_blueprint.route("/orders/<int:order_id>")
def get_one_order_views(order_id):
    try:
        return jsonify(get_one_order(order_id))
    except AttributeError:
        return abort(404, ValueError("No such order found|Такой заказ не найден"))


@movie_blueprint.route("/offers")
def get_all_offers_views():
    return jsonify(get_all_offers())


@movie_blueprint.route("/offers/<int:offer_id>")
def get_one_offer_views(offer_id):
    try:
        return jsonify(get_one_offer(offer_id))
    except AttributeError:
        return abort(404, ValueError("No such offer found|Такое предложение не найдено"))