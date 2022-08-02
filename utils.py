from flask import Flask
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


def get_all_users():
    return [row.to_dict() for row in User.query.all()]


def get_one_user(user_id):
    return db.session.query(User).get(user_id).to_dict()


def get_all_orders():
    return [row.to_dict() for row in Order.query.all()]


def get_one_order(order_id):
    return db.session.query(Order).get(order_id).to_dict()


def get_all_offers():
    return [row.to_dict() for row in Offer.query.all()]


def get_one_offer(offer_id):
    return db.session.query(Offer).get(offer_id).to_dict()


db.drop_all()
db.create_all()
