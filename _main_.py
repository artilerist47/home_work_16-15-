import json

from flask import Flask, jsonify, abort
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
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(20))
    phone = db.Column(db.String(15))

    def to_dict(self):
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

    def to_dict(self):
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

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


def get_data_user(input_data):
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


def get_data_order(input_data):
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


def get_data_offer(input_data):
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


def get_all(selected_model):
    return [row.to_dict() for row in db.session.query(selected_model)]


# def get_all_users():
#     return [row.to_dict() for row in User.query.all()]

    # result = []
    # for row in User.query.all():
    #     result.append(row.to_dict())
    # return result


# def get_all_orders():
#     return [row.to_dict() for row in Order.query.all()]

    # result = []
    # for row in Order.query.all():
    #     result.append(row.to_dict())
    # return result


# def get_all_offers():
#     return [row.to_dict() for row in Offer.query.all()]

    # result = []
    # for row in Offer.query.all():
    #     result.append(row.to_dict())
    # return result


def get_one_user(user_id):
    # return db.session.query(User).filter(User.id == user_id).first().to_dict()

    return db.session.query(User).get(user_id).to_dict()

    # return [row for row in get_all_users() if row.get("id") == user_id]

    # data = get_all_users()
    # for row in data:
    #     if row.get('id') == user_id:
    #         return row


def get_one_order(order_id):
    # return db.session.query(Order).filter(Order.id == order_id).first().to_dict()

    return db.session.query(Order).get(order_id).to_dict()

    # return [row for row in get_all_orders() if row.get("id") == order_id]

    # data = get_all_orders()
    # for row in data:
    #     if row.get('id') == user_id:
    #         return row



def get_one_offer(offer_id):
    # return db.session.query(Offer).filter(Offer.id == offer_id).first().to_dict()

    return db.session.query(Offer).get(offer_id).to_dict()

    # return [row for row in get_all_offers() if row.get("id") == offer_id]

    # data = get_all_offers()
    # for row in data:
    #     if row.get('id') == user_id:
    #         return row


db.drop_all()
db.create_all()

with open("users.json", encoding='utf-8') as file:
    get_data_user(json.load(file))

with open("orders.json", encoding='utf-8') as file:
    get_data_order(json.load(file))

with open("offers.json") as file:
    get_data_offer(json.load(file))


@app.route("/users")
def get_all_users_views():
    # return jsonify(get_all_users())
    return jsonify(get_all(User))


@app.route("/orders")
def get_all_orders_views():
    # return jsonify(get_all_orders())
    return jsonify(get_all(Order))


@app.route("/offers")
def get_all_offers_views():
    # return jsonify(get_all_offers())
    return jsonify(get_all(Offer))


@app.route("/users/<int:user_id>")
def get_one_user_views(user_id):
    try:
        return jsonify(get_one_user(user_id))
    except AttributeError:
        return abort(404, ValueError("No such user found|Такой пользователь не найден"))


@app.route("/orders/<int:order_id>")
def get_one_order_views(order_id):
    try:
        return jsonify(get_one_order(order_id))
    except AttributeError:
        return abort(404, ValueError("No such order found|Такой заказ не найден"))


@app.route("/offers/<int:offer_id>")
def get_one_offer_views(offer_id):
    try:
        return jsonify(get_one_offer(offer_id))
    except AttributeError:
        return abort(404, ValueError("No such offer found|Такое предложение не найдено"))


if __name__ == "__main__":
    app.run()
