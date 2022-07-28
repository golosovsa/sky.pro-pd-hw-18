"""
    DAO abstraction level for movie
"""


class MovieDAO:
    """ CRUD interface for Movie """

    def __init__(self, session):
        self.session = session

