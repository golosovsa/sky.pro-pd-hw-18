"""
    Base Service class
"""
from app.dao.base_dao import BaseDAO


class ServiceException(Exception):
    """ Service exception """
    def __init__(self, message):
        super().__init__(message)


class ServiceLogger:
    """ Service logger decorator """
    def __init__(self, method):
        self._method = method

    def __call__(self):

        def wrapper(*args, **kwargs):
            try:
                result = self._method(*args, **kwargs)
            except Exception as e:
                self.logger(e)
                raise ServiceException("Service abstraction level error")
            return result

        return wrapper

    def logger(self, exception):
        pass


class BaseService:
    """ Base service class with base business logic """

    def __init__(self, dao: BaseDAO):
        self._dao = dao

    @ServiceLogger
    def create(self, data):
        """ Create method"""
        return self._dao.create(data)

    @ServiceLogger
    def read_all(self, limit: int or None = None, offset: int or None = None):
        """ Read all method """
        return self._dao.read_all(limit=limit, offset=offset)

    @ServiceLogger
    def read_one(self, pk):
        """ Read one method """
        return self._dao.read_one(pk)

    @ServiceLogger
    def update(self, pk, data):
        """ Update method """
        model = self._dao.read_one(pk)
        for field in self._dao.fields:
            setattr(model, field, data[field])
        return self._dao.update(model)

    @ServiceLogger
    def partial_update(self, pk, data):
        """ Partial update method """
        model = self._dao.read_one(pk)
        for field in self._dao.fields:
            if field in data:
                setattr(model, field, data[field])

        self._dao.update(model)

    @ServiceLogger
    def delete(self, pk):
        """ Delete method """
        model = self._dao.read_one(pk)
        self._dao.delete(model)
