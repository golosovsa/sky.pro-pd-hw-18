"""
    SQLAlchemy movie models
"""

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

    genres = db.relationship("Genre", back_populates="movies")
    directors = db.relationship("Director", back_populates="movies")

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

