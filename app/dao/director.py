"""
    DAO abstraction level for director
"""

from .base_dao import BaseDAO
from .model.director import Director


class DirectorDAO(BaseDAO):
    """ CRUD interface for Movie """

    def __init__(self, session):
        super().__init__(Director, session)
        self._updatable_fields = [
            "name",
        ]
