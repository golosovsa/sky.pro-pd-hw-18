"""
    SQLAlchemy movie models
"""
from marshmallow import Schema, fields

from app.setup_db import db


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    trailer = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.id"), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"), nullable=False)

    genre = db.relationship("Genre", back_populates="movies")
    director = db.relationship("Director", back_populates="movies")

    def __repr__(self):
        return f"Movie(\n" \
               f"    '{self.title}',\n" \
               f"    '{self.description}',\n" \
               f"    '{self.trailer}',\n" \
               f"    {self.year},\n" \
               f"    {self.rating},\n" \
               f"    {self.genre_id},\n" \
               f"    {self.director_id}\n" \
               f")"


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

    genre = fields.Pluck("GenreSchema", "name")
    director = fields.Pluck("DirectorSchema", "name")
