"""
    Service abstraction level for genre
"""
from app.service.base_service import BaseService


class GenreService(BaseService):

    def __init__(self, dao):
        super(GenreService, self).__init__(dao)



