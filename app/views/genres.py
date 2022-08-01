"""
    Genres restX namespace

"""

from flask import jsonify
from flask_restx import Namespace, Resource, fields

from app.dao.model.genre import GenreSchema
from app.service_container import genre_service

genres_ns = Namespace("genres", description="API route for genre entities")

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

genre_entity_fields = genres_ns.model("Genre Entity", {
    "name": fields.String(),
})


@genres_ns.doc(model=genre_entity_fields)
@genres_ns.route("/")
class GenresView(Resource):

    @genres_ns.doc(description="Get all genres")
    def get(self):
        data = genre_service.read_all()
        return genres_schema.dump(data), 200


@genres_ns.route("/<int:pk>")
class GenreView(Resource):

    @genres_ns.doc(description="Get genre by id")
    def get(self, pk):
        data = genre_service.read_one(pk)
        return genre_schema.dump(data), 200
