import json

from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    """
    Модель - пользователь
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15))
    last_name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(20))
    phone = db.Column(db.String(15))

    def view(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    """
    Модель - заказ
    :param: customer_id - ID пользователя
    :param: executor_id - ID исполнителя
    """
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    description = db.Column(db.String(15))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    address = db.Column(db.String(50))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey(f'{User.__tablename__}.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey(f'{User.__tablename__}.id'))

    def view(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    """
    Модель - предложение
    :param: order_id - ID заказа
    :param: executor_id - ID исполнителя
    """
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(f'{Order.__tablename__}.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey(f'{User.__tablename__}.id'))

    def view(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


def enter_user_data(input_data):
    """
    Получаем данные о пользователей
    :param input_data: загружаемые данные пользователей
    """
    for row in input_data:
        db.session.add(
            User(
                id=row.get("id"),
                first_name=row.get("first_name"),
                last_name=row.get("last_name"),
                age=row.get("age"),
                email=row.get("email"),
                role=row.get("role"),
                phone=row.get("phone")
            )
        )
    db.session.commit()


def enter_order_data(input_data):
    """
    Получаем данные заказа
    :param input_data: загружаемые данные предложения
    """
    for row in input_data:
        db.session.add(
            Order(
                id=row.get("id"),
                name=row.get('name'),
                description=row.get("description"),
                start_date=row.get("start_date"),
                end_date=row.get("end_date"),
                address=row.get("address"),
                price=row.get("price"),
                customer_id=row.get("customer_id"),
                executor_id=row.get("executor_id")
            )
        )
    db.session.commit()


def enter_offer_data(input_data):
    """
    Получаем данные предложений
    :param input_data: загружаемые данные предложений
    """
    for row in input_data:
        db.session.add(
            Offer(
                id=row.get("id"),
                order_id=row.get("order_id"),
                executor_id=row.get("executor_id"),
            )
        )
    db.session.commit()


db.drop_all()
db.create_all()

with open("users.json", encoding='utf-8') as file:
    enter_user_data(json.load(file))

with open("orders.json", encoding='utf-8') as file:
    enter_order_data(json.load(file))

with open("offers.json") as file:
    enter_offer_data(json.load(file))


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


if __name__ == "__main__":
    app.run()
