from flask import request, jsonify, abort

from app import db, app
from models import User, Order, Offer
from utils import enter_user_data, enter_order_data, enter_offer_data


@app.route("/users", methods=["GET", "POST"])
def get_all_users_views():
    if request.method == "GET":
        return jsonify([user_response.view() for user_response in db.session.query(User)])
    elif request.method == "POST":
        enter_user_data([request.json])
        return jsonify(request.json)


@app.route("/orders", methods=["GET", "POST"])
def get_all_orders_views():
    if request.method == "GET":
        return jsonify([user_response.view() for user_response in db.session.query(Order)])
    elif request.method == "POST":
        enter_order_data([request.json])
        return jsonify(request.json)


@app.route("/offers", methods=["GET", "POST"])
def get_all_offers_views():
    if request.method == "GET":
        return jsonify([user_response.view() for user_response in db.session.query(Offer)])
    elif request.method == "POST":
        enter_offer_data([request.json])
        return jsonify(request.json)


@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def get_one_user_views(user_id):
    if request.method == "GET":
        try:
            return jsonify(db.session.query(User).get(user_id).view())
        except AttributeError:
            return abort(404, ValueError("No such user found|Такой пользователь не найден"))
    elif request.method == "PUT":
        db.session.query(User).filter(User.id == user_id).update(request.json)
        db.session.commit()
        return jsonify(f"Данные обновлены:", request.json)
    elif request.method == "DELETE":
        db.session.delete(db.session.query(User).get(user_id))
        db.session.commit()
        return jsonify(f"Данные пользователя удалены")


@app.route("/orders/<int:order_id>", methods=["GET", "PUT", "DELETE"])
def get_one_order_views(order_id):
    if request.method == "GET":
        try:
            return jsonify(db.session.query(Order).get(order_id).view())
        except AttributeError:
            return abort(404, ValueError("No such order found|Такой заказ не найден"))
    elif request.method == "PUT":
        db.session.query(Order).filter(Order.id == order_id).update(request.json)
        db.session.commit()
        return jsonify(f"Данные обновлены:", request.json)
    elif request.method == "DELETE":
        db.session.delete(db.session.query(Order).get(order_id))
        db.session.commit()
        return jsonify(f"Данные заказа удалены")


@app.route("/offers/<int:offer_id>", methods=["GET", "PUT", "DELETE"])
def get_one_offer_views(offer_id):
    if request.method == "GET":
        try:
            return jsonify(db.session.query(Offer).get(offer_id).view())
        except AttributeError:
            return abort(404, ValueError("No such offer found|Такое предложение не найдено"))
    elif request.method == "PUT":
        db.session.query(Offer).filter(Offer.id == offer_id).update(request.json)
        db.session.commit()
        return jsonify(f"Данные обновлены:", request.json)
    elif request.method == "DELETE":
        db.session.delete(db.session.query(Offer).get(offer_id))
        db.session.commit()
        return jsonify(f"Данные предложения удалены")