"""
    SQLAlchemy Director model
"""
from marshmallow import Schema, fields

from app.setup_db import db


class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    movies = db.relationship("Movie", back_populates="directors")

    def __repr__(self):
        return f"Director({self.id}, '{self.name}')"


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()
