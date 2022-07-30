"""
    DAO abstraction level for genre
"""

from .base_dao import BaseDAO
from .model.genre import Genre


class GenreDAO(BaseDAO):
    """ CRUD interface for Movie """

    def __init__(self, session):
        super().__init__(Genre, session)
        self._updatable_fields = [
            "name",
        ]
