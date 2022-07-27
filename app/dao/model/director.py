"""
    SQLAlchemy Director model
"""

from app.setup_db import db


class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    movies = db.Relationship("Movie", back_population="directors")
