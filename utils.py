import json

from app import db
from models import User, Order, Offer


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