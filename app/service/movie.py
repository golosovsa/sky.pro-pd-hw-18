"""
    Service abstraction level for director
"""
from app.service.base_service import BaseService, ServiceException
from app.dao.movie import MovieDAO


class MovieService(BaseService):

    def __init__(self, dao: MovieDAO):
        super().__init__(dao)
        self._dao: MovieDAO = dao

    def cast_extra(self, extra: any, type_of):
        try:
            return type_of(extra)
        except ValueError as exception:
            self.logger(ValueError, exception, None)
            raise ServiceException("Extra key error during type casting, invalid extra key", code=400)

    def read_all(self,
                 limit: int or None = None,
                 offset: int or None = None,
                 filter_by: str or None = None,
                 extra: any = None):

        if not filter_by:
            return super(MovieService, self).read_all(offset=offset, limit=limit)

        elif filter_by == "director":
            return self._dao.filter_by_director(director_id=self.cast_extra(extra, int), limit=limit, offset=offset)

        elif filter_by == "genre":
            return self._dao.filter_by_genre(genre_id=self.cast_extra(extra, int), limit=limit, offset=offset)

        elif filter_by == "title":
            return self._dao.filter_by_title(title=self.cast_extra(extra, str), limit=limit, offset=offset)

        elif filter_by == "description":
            return self._dao.filter_by_description(description=self.cast_extra(extra, str), limit=limit, offset=offset)

        elif filter_by == "year":
            return self._dao.filter_by_year(year=self.cast_extra(extra, int), limit=limit, offset=offset)

        elif filter_by == "rating":
            return self._dao.filter_by_rating(rating=self.cast_extra(extra, float), limit=limit, offset=offset)

        raise ServiceException("Invalid filter_by key")
