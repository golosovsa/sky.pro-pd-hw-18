# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

# Пример

# from flask import Flask
# from flask_restx import Api
#
# from config import Config
# from models import Review, Book
# from setup_db import db
# from views.books import book_ns
# from views.reviews import review_ns
#
# функция создания основного объекта app
# def create_app(config_object):
#     app = Flask(__name__)
#     app.config.from_object(config_object)
#     register_extensions(app)
#     return app
#
#
# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
# def register_extensions(app):
#     db.init_app(app)
#     api = Api(app)
#     api.add_namespace(...)
#     create_data(app, db)
#
#
# функция
# def create_data(app, db):
#     with app.app_context():
#         db.create_all()
#
#         создать несколько сущностей чтобы добавить их в БД
#
#         with db.session.begin():
#             db.session.add_all(здесь список созданных объектов)
#
#
# app = create_app(Config())
# app.debug = True
#
# if __name__ == '__main__':
#     app.run(host="localhost", port=10001, debug=True)
from flask import Flask
from flask_restx import Api
from sqlalchemy.orm import Session

from app.config import Config
from app.views.movies import movies_ns
from app.views.directors import directors_ns
from app.views.genres import genres_ns
from app.setup_db import db
from app.dao.model.movie import Movie
from app.dao.model.genre import Genre
from app.dao.model.director import Director
from app.constants import TEST_DB_DIRECTORS, TEST_DB_GENRES


def create_app(config_object: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config_object)
    application.app_context().push()
    return application


def register_extensions(application: Flask):
    db.init_app(application)
    api = Api()
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.init_app(application)


def fill_data(application: Flask):
    with application.app_context():
        db.create_all()
        db.session.commit()

        session: Session = db.session

        for i in range(TEST_DB_DIRECTORS):
            session.add(Director(name=f"Test Director {i}"))

        for i in range(TEST_DB_GENRES):
            session.add(Director(name=f"Test Director {i}"))


app = create_app(Config())
register_extensions(app)
fill_data(app)

if __name__ == "__main__":

    app.run(debug=True)
