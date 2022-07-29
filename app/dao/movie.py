"""
    DAO abstraction level for movie
"""

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

    def filter_by_title(self, title, limit=None, offset=None, query=None):
        query = query or self.get_query()
        query = query.filter(Movie.title.like(f"%title%"))
        return self.read_all(limit=limit, offset=offset, query=query)


movie_dao = MovieDAO(None)
director_dao = MovieDAO(None)
genre_dao = MovieDAO(None)


class Sample:

    def foo(self, data):
        with movie_dao as transaction:
            try:
                director_dao.create(data["new_director"], transaction=transaction)
                genre_dao.create(data["new_director"], transaction=transaction)
                movie_dao.create(data["new_director"], transaction=transaction)
            except Exception as e:
                genre_dao
