"""
    Base DAO class
"""

from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import SQLAlchemyError


class BaseDAO:
    """ Base CRUD interface """

    def __init__(self, model_type: type, session: Session):
        self._Model = model_type
        self._session: Session = session
        self._nested_session: Session = None
        self._updatable_fields = []

    @staticmethod
    def logger(exc_type, exc_val, exc_tb):
        """ Logger errors DAO abstraction level """
        pass

    def get_query(self, transaction=None) -> Query:
        """ Get new query object """
        return self._session.query(self._Model) if not transaction else transaction.query(self._Model)

    def commit_nested(self):
        self._nested_session.commit()

    def create_nested(self, transaction: Session, data: dict):
        """ Nested create model method """
        model = self._Model(**data)
        transaction.add(model)

    def read_all_nested(self, query: Query, transaction: Session, limit: int = None, offset: int = None):
        """ Nested read all models method """
        query = query or self.get_query(transaction)

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return query.all()

    def read_one_nested(self, transaction: Session, pk: int):
        """ Nested read one method """
        query: Query = self.get_query(transaction)
        return query.get(pk)

    def update_nested(self, transaction: Session, data: dict):
        """ Nested update method """

        pk = data.get("id", None)
        if pk is None:
            raise DAOException("Update error, id field not found")

        model = self.read_one_nested(transaction, pk)
        for field in self._updatable_fields:
            setattr(model, field, data.get(field, None))

        transaction.add(model)

    def delete_nested(self, transaction: Session, pk):
        """ Nested delete method """
        model = self.read_one_nested(transaction, pk)
        transaction.delete(model)

    def __enter__(self):
        """ Start nested transaction """
        self._nested_session = self._session.begin_nested()
        return self._nested_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Close nested transaction """
        if exc_type:
            self._nested_session.rollback()
            self.logger(exc_type, exc_val, exc_tb)
            self._nested_session.close()
            self._nested_session = None
            raise DAOException("Something went wrong at the DAO abstraction layer")

        if len(self._nested_session.new) or len(self._nested_session.deleted) or len(self._nested_session.dirty):
            self._nested_session.rollback()
            self._nested_session.close()
            self._nested_session = None
            raise DAOException("Commit pending but not executed")

        self._nested_session.close()
        self._nested_session = None

        return True

    def create(self, data):
        with self as transaction:
            self.create_nested(transaction, data)
            self.commit_nested()

    def read_all(self, query=None, offset: int or None = None, limit: int or None = None):
        with self as transaction:
            data = self.read_all_nested(query, transaction, limit, offset)

        return data

    def read_one(self, pk):
        with self as transaction:
            data = self.read_one_nested(transaction, pk)


class DAOException(Exception):
    """ DAO exception """
    def __init__(self, message):
        super().__init__(message)
