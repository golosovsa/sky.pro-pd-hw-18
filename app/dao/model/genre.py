"""
    SQLAlchemy Genre model
"""

from app.setup_db import db


class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)

    movies = db.Relationship("Movie", back_population="genres")
