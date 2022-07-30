"""
    Service abstraction level for director
"""
from app.service.base_service import BaseService


class DirectorService(BaseService):

    def __init__(self, dao):
        super(DirectorService, self).__init__(dao)

