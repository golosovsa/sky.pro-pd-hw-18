"""
    Service abstraction level for director
"""
from app.service.base_service import BaseService


class MovieService(BaseService):

    def __init__(self, dao):
        super(MovieService, self).__init__(dao)

