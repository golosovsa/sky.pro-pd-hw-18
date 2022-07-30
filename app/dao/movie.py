"""
    DAO abstraction level for movie
"""
from sqlalchemy.orm import Query, Session

from .base_dao import BaseDAO
from .model.movie import Movie


class MovieDAO(BaseDAO):
    """ CRUD interface for Movie """

    def __init__(self, session):
        super().__init__(Movie, session)
        self._updatable_fields = [
            "title",
            "description",
            "trailer",
            "year",
            "rating",
            "genre_id",
            "director_id",
        ]

    def filter_by_director_nested(self,
                                  transaction: Session,
                                  director_id: int,
                                  query: Query or None = None,
                                  limit: int or None = None,
                                  offset: int or None = None):
        query: Query = query or self.get_query(transaction)
        query: Query = query.filter(Movie.director_id == director_id)
        return self.read_all_nested(transaction, query, limit, offset)

    def filter_by_director(self, director_id: int, limit: int or None = None, offset: int or None = None):
        return self.filter_by_director_nested(self._session, director_id, limit=limit, offset=offset)

    def filter_by_genre_nested(self,
                               transaction: Session,
                               genre_id: int,
                               query: Query or None = None,
                               limit: int or None = None,
                               offset: int or None = None
                               ):
        query: Query = query or self.get_query(transaction)
        query: Query = query.filter(Movie.genre_id == genre_id)
        return self.read_all_nested(transaction, query, limit, offset)

    def filter_by_genre(self, genre_id: int, limit: int or None = None, offset: int or None = None):
        return self.filter_by_genre_nested(self._session, genre_id, limit=limit, offset=offset)


movies_dao = MovieDAO(None)
directors_dao = MovieDAO(None)
genres_dao = MovieDAO(None)

class Test:
    def test(self, data):
        with movies_dao as transaction:
            director = directors_dao.create_nested(transaction, data["director"])
            genre = genres_dao.create_nested(transaction, data["genre"])
            data["movie"]["director_id"] = director.id
            data["movie"]["genre_id"] = genre.id
            movie = movies_dao.create_nested(transaction, data["movie"])
            movies_dao.commit_nested(transaction)
