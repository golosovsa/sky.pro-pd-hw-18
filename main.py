"""
    main app
"""

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
from app.constants import TEST_MOVIES


def create_app(config_object: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config_object)
    application.app_context().push()
    return application


def register_extensions(application: Flask):
    db.init_app(application)
    api = Api(description="Homework 18")
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.init_app(application)


def fill_data(application: Flask):
    with application.app_context():
        db.create_all()
        db.session.commit()

        session: Session = db.session

        genres = [Genre(name=genre) for genre in set([movie["genre"] for movie in TEST_MOVIES])]
        directors = [Director(name=director) for director in set([movie["director"] for movie in TEST_MOVIES])]

        session.add_all(genres)
        session.add_all(directors)

        session.commit()

        movies = []

        for movie in TEST_MOVIES:

            genre_id = None
            for genre in genres:
                if genre.name == movie["genre"]:
                    genre_id = genre.id
                    break

            director_id = None
            for director in directors:
                if director.name == movie["director"]:
                    director_id = director.id
                    break

            del movie["genre"]
            del movie["director"]

            movies.append(
                Movie(**movie,
                      director_id=director_id,
                      genre_id=genre_id)
            )

        session.add_all(movies)
        session.commit()


app = create_app(Config())
register_extensions(app)
fill_data(app)

if __name__ == "__main__":
    app.run(debug=True)
