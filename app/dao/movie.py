"""
    DAO abstraction level for movie
"""
from sqlalchemy.orm import Query, SessionTransaction

from .base_dao import BaseDAO
from .model.movie import Movie
from app.constants import EPSILON


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
                                  transaction: SessionTransaction or None,
                                  director_id: int,
                                  query: Query or None = None,
                                  limit: int or None = None,
                                  offset: int or None = None):
        query: Query = query or self.get_query(transaction)
        query: Query = query.filter(Movie.director_id == director_id)
        return self.read_all_nested(transaction, query, limit, offset)

    def filter_by_director(self, director_id: int, limit: int or None = None, offset: int or None = None):
        return self.filter_by_director_nested(None, director_id, limit=limit, offset=offset)

    def filter_by_genre_nested(self,
                               transaction: SessionTransaction or None,
                               genre_id: int,
                               query: Query or None = None,
                               limit: int or None = None,
                               offset: int or None = None
                               ):
        query: Query = query or self.get_query(transaction)
        query: Query = query.filter(Movie.genre_id == genre_id)
        return self.read_all_nested(transaction, query, limit, offset)

    def filter_by_genre(self, genre_id: int, limit: int or None = None, offset: int or None = None):
        return self.filter_by_genre_nested(None, genre_id, limit=limit, offset=offset)

    def filter_by_title_nested(self,
                               transaction: SessionTransaction or None,
                               title: str,
                               query: Query or None = None,
                               limit: int or None = None,
                               offset: int or None = None):
        query: Query = query or self.get_query(transaction)
        query: Query = query.filter(Movie.title.like(f"%{title}%"))
        return self.read_all_nested(transaction, query, limit, offset)

    def filter_by_title(self, title: str, limit: int or None = None, offset: int or None = None):
        return self.filter_by_title_nested(None, title, limit=limit, offset=offset)

    def filter_by_description_nested(self,
                                     transaction: SessionTransaction or None,
                                     description: str,
                                     query: Query or None = None,
                                     limit: int or None = None,
                                     offset: int or None = None):
        query: Query = query or self.get_query(transaction)
        query: Query = query.filter(Movie.description.like(f"%{description}%"))
        return self.read_all_nested(transaction, query, limit, offset)

    def filter_by_description(self, description: str, limit: int or None = None, offset: int or None = None):
        return self.filter_by_description_nested(None, description, limit=limit, offset=offset)

    def filter_by_year_nested(self,
                              transaction: SessionTransaction or None,
                              year: int,
                              query: Query or None = None,
                              limit: int or None = None,
                              offset: int or None = None):
        query: Query = query or self.get_query(transaction)
        query: Query = query.filter(Movie.year == year)
        return self.read_all_nested(transaction, query, limit, offset)

    def filter_by_year(self, year: int, limit: int or None = None, offset: int or None = None):
        return self.filter_by_year_nested(None, year, limit=limit, offset=offset)

    def filter_by_rating_nested(self,
                                transaction: SessionTransaction or None,
                                rating: float,
                                query: Query or None = None,
                                limit: int or None = None,
                                offset: int or None = None):
        query: Query = query or self.get_query(transaction)
        query: Query = query.filter(rating - EPSILON < Movie.rating, rating + EPSILON > Movie.rating)
        return self.read_all_nested(transaction, query, limit, offset)

    def filter_by_rating(self, rating: float, limit: int or None = None, offset: int or None = None):
        return self.filter_by_rating_nested(None, rating, limit=limit, offset=offset)


