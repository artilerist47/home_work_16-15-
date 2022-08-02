import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from main_views import movie_blueprint
from utils import get_data_user, get_data_order, get_data_offer

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.register_blueprint(movie_blueprint)


db.drop_all()
db.create_all()


with open("users.json", encoding='utf-8') as file:
    get_data_user(json.load(file))

with open("orders.json", encoding='utf-8') as file:
    get_data_order(json.load(file))

with open("offers.json") as file:
    get_data_offer(json.load(file))


if __name__ == "__main__":
    app.run()
