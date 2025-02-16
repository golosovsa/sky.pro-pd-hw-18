"""
    SQLAlchemy Genre model
"""
from marshmallow import Schema, fields

from app.setup_db import db


class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    movies = db.relationship("Movie", back_populates="genre")

    def __repr__(self):
        return f"Genre({self.id}, '{self.name}')"


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
