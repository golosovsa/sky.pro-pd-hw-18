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
        self._nested_session: Session or None = None
        self._updatable_fields = []

    @staticmethod
    def logger(exc_type, exc_val, exc_tb):
        """ Logger errors DAO abstraction level """
        pass

    def get_query(self, transaction=None) -> Query:
        """ Get new query object """
        return self._session.query(self._Model) if not transaction else transaction.query(self._Model)

    def commit_nested(self, transaction: Session = None):
        """ Nested commit method """
        transaction = transaction or self._nested_session
        transaction.commit()

    def create_nested(self, transaction: Session, data: dict):
        """ Nested create model method """
        model = self._Model(**data)
        transaction.add(model)
        return model

    def read_all_nested(self,
                        transaction: Session,
                        query: Query,
                        limit: int or None = None,
                        offset: int or None = None):
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

    def update_nested(self, transaction: Session, pk: int, data: dict):
        """ Nested update method """

        data["id"] = pk

        model = self.read_one_nested(transaction, pk)
        for field in self._updatable_fields:
            setattr(model, field, data.get(field, None))

        transaction.add(model)

        return model

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
        """ Create method """
        with self as transaction:
            model = self.create_nested(transaction, data)
            self.commit_nested(transaction)

        return model

    def read_all(self, query=None, offset: int or None = None, limit: int or None = None):
        """ Read all method """
        with self as transaction:
            data = self.read_all_nested(query, transaction, limit, offset)

        return data

    def read_one(self, pk: int):
        """ Read one method """
        with self as transaction:
            data = self.read_one_nested(transaction, pk)

        return data

    def update(self, pk: int, data: dict):
        """ Update method """
        with self as transaction:
            model = self.update_nested(transaction, pk, data)
            self.commit_nested(transaction)

        return model

    def delete(self, pk: int):
        """ Delete method """
        with self as transaction:
            self.delete_nested(transaction, pk)
            self.commit_nested(transaction)


class DAOException(Exception):
    """ DAO exception """
    def __init__(self, message):
        super().__init__(message)
