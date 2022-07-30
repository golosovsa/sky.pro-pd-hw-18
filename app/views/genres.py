"""
    Genres restX namespace

"""

from flask import jsonify
from flask_restx import Namespace, Resource

from app.dao.model.genre import GenreSchema
from app.service_container import genre_service

genres_ns = Namespace("genres")

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route("/")
class GenresView(Resource):
    def get(self):
        data = genre_service.read_all()
        return genres_schema.dump(data), 200


@genres_ns.route("/<int:pk>")
class GenreView(Resource):

    def get(self, pk):
        data = genre_service.read_one(pk)
        return genre_schema.dump(data), 200

