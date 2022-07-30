"""
    Base Service class
"""
from functools import wraps

from app.dao.base_dao import BaseDAO


class ServiceException(Exception):
    """ Service exception """
    def __init__(self, message):
        super().__init__(message)


class BaseService:
    """ Base service class with base business logic """

    def __init__(self, dao: BaseDAO):
        self._dao = dao

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger(exc_type, exc_val, exc_tb)
            raise ServiceException("Something went wrong at the SERVICE abstraction layer")

        return True

    def logger(self, exc_type, exc_val, exc_tb):
        pass

    def create(self, data):
        """ Create method"""
        with self:
            return self._dao.create(data)

    def read_all(self, limit: int or None = None, offset: int or None = None):
        """ Read all method """
        with self:
            return self._dao.read_all(limit=limit, offset=offset)

    def read_one(self, pk):
        """ Read one method """
        with self:
            return self._dao.read_one(pk)

    def update(self, pk, data):
        """ Update method """
        with self:
            model = self._dao.read_one(pk)
            for field in self._dao.fields:
                setattr(model, field, data[field])
            return self._dao.update(model)

    def partial_update(self, pk, data):
        """ Partial update method """
        with self:
            model = self._dao.read_one(pk)
            for field in self._dao.fields:
                if field in data:
                    setattr(model, field, data[field])

            return self._dao.update(model)

    def delete(self, pk):
        """ Delete method """
        with self:
            model = self._dao.read_one(pk)
            self._dao.delete(model)


