"""
    Base DAO class
"""

from sqlalchemy.orm import Session, Query, SessionTransaction


class BaseDAO:
    """ Base CRUD interface """

    def __init__(self, model_type: type, session: Session):
        self._Model = model_type
        self._session: Session = session
        self._nested_session: Session or None = None
        self._updatable_fields = []

    @property
    def fields(self):
        return self._updatable_fields

    @staticmethod
    def logger(exc_type, exc_val, exc_tb):
        """ Logger errors DAO abstraction level """
        pass

    def get_query(self, transaction: SessionTransaction or None = None) -> Query:
        """ Get new query object """
        return self._session.query(self._Model) if not transaction else transaction.session.query(self._Model)

    def commit_nested(self, transaction: SessionTransaction or None = None):
        """ Nested commit method """
        transaction = transaction or self._nested_session
        transaction.commit()

    def create_nested(self, transaction: SessionTransaction, data: dict):
        """ Nested create model method """
        model = self._Model(**data)
        transaction.session.add(model)
        return model

    def read_all_nested(self,
                        transaction: SessionTransaction,
                        query: Query or None = None,
                        limit: int or None = None,
                        offset: int or None = None):
        """ Nested read all models method """
        query = query or self.get_query(transaction)

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return query.all()

    def read_one_nested(self, transaction: SessionTransaction, pk: int):
        """ Nested read one method """
        query: Query = self.get_query(transaction)
        return query.get(pk)

    def update_nested(self, transaction: Session, model):
        """ Nested update method """
        transaction.session.add(model)
        return model

    def delete_nested(self, transaction: SessionTransaction, model):
        """ Nested delete method """
        transaction.session.delete(model)

    def __enter__(self):
        """ Start nested transaction """
        self._nested_session = self._session.begin_nested()
        return self._nested_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Close nested transaction """
        if exc_type:
            self._nested_session.rollback()
            self.logger(exc_type, exc_val, exc_tb)
            self._nested_session = None
            raise DAOException("Something went wrong at the DAO abstraction layer")

        if \
                len(self._nested_session.session.new) or \
                len(self._nested_session.session.deleted) or \
                len(self._nested_session.session.dirty):
            self._nested_session.rollback()
            self._nested_session = None
            raise DAOException("Commit pending but not executed")

        self._nested_session = None

        return True

    def create(self, data):
        """ Create method """
        with self as transaction:
            model = self.create_nested(transaction, data)
            self.commit_nested(transaction)

        return model

    def read_all(self, offset: int or None = None, limit: int or None = None):
        """ Read all method """
        with self as transaction:
            data = self.read_all_nested(transaction, None, limit, offset)

        return data

    def read_one(self, pk: int):
        """ Read one method """
        with self as transaction:
            data = self.read_one_nested(transaction, pk)

        return data

    def update(self, model):
        """ Update method """
        with self as transaction:
            model = self.update_nested(transaction, model)
            self.commit_nested(transaction)

        return model

    def delete(self, model):
        """ Delete method """
        with self as transaction:
            self.delete_nested(transaction, model)
            self.commit_nested(transaction)


class DAOException(Exception):
    """ DAO exception """

    def __init__(self, message):
        super().__init__(message)
