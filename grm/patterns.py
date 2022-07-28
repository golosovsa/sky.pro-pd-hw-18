"""
    My patterns library
"""

from http import HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from flask_restx.errors import abort


class BaseDAO:
    """ Base CRUD interface """
    session: Session = None

    def __init__(self, model_type):
        self.Model = model_type

    def logger(self, e: Exception or str):
        pass

    def create(self, data):

        model = self.Model(**data)

        try:
            with self.session:
                self.session.add(model)
                self.session.commit()

        except SQLAlchemyError as e:

            self.logger(e)

            abort(*HTTPStatus.INTERNAL_SERVER_ERROR)

    def read_all(self, limit: int = None, offset: int = None):

        data = None

        try:

            query = self.session.query(self.Model)

            if limit:
                query.limit(limit)

            if offset:
                query.offset(offset)

            data = query.all()

        except SQLAlchemyError as e:

            self.logger(e)

            abort(*HTTPStatus.INTERNAL_SERVER_ERROR)

        if data:
            return data

        abort(*HTTPStatus.NOT_FOUND)

    def read_one(self, pk):

        data = None

        try:
            data = self.session.query(self.Model).get(pk)

        except SQLAlchemyError as e:

            self.logger(e)

            abort(*HTTPStatus.INTERNAL_SERVER_ERROR)

        if data:
            return data

        abort(*HTTPStatus.NOT_FOUND)

    def update(self, data: dict):

        pk = data.get("id", None)

        if pk is None:
            self.logger("Entity id not found")
            abort(*HTTPStatus.NOT_FOUND)

        model = self.read_one(pk)

        model.update
