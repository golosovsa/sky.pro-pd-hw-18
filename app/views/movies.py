"""
    Movies restX namespace

"""

from flask_restx import Namespace, Resource, fields
from flask import request

from app.dao.model.movie import MovieSchema
from app.service_container import movie_service

movies_ns = Namespace("movies", description="API route for movie entities")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

arguments = movies_ns.parser()
arguments.add_argument(
    "offset",
    type=int,
    help="Database table offset",
    location="args"
)
arguments.add_argument(
    "limit",
    type=int,
    help="Database table limit",
    location="args"
)
arguments.add_argument(
    "filter_by",
    type=str,
    help="For filter by query. Bad choice: {error_msg}",
    location="args",
    choices=(
        "director",
        "genre",
        "title",
        "description",
        "year",
        "rating",
    ),
)
arguments.add_argument(
    "extra",
    type=str,
    help="Extra key",
    location="args"
)

movie_entity_fields = movies_ns.model("Movie Entity", {
    "title": fields.String(),
    "description": fields.String(),
    "trailer": fields.String(),
    "year": fields.Integer(),
    "rating": fields.Float(),
    "genre_id": fields.Integer(),
    "director_id": fields.Integer(),
})

@movies_ns.route("/")
class MoviesView(Resource):

    @movies_ns.doc(description="Get all movies")
    @movies_ns.expect(arguments)
    def get(self):

        args = arguments.parse_args()
        limit = args.get("limit")
        offset = args.get("offset")
        filter_by = args.get("filter_by")
        extra = args.get("extra")

        movie = movie_service.read_all(limit=limit, offset=offset, filter_by=filter_by, extra=extra)

        return movies_schema.dump(movie), 200

    @movies_ns.doc(description="Create new movie from json")
    @movies_ns.expect(movie_entity_fields)
    def post(self):
        data = request.json
        movie = movie_service.create(data)
        return {}, 201, {"location": f"/movies/{movie.id}"}


@movies_ns.route("/<int:pk>")
class MovieView(Resource):

    @movies_ns.doc(description="Get one movie by id")
    def get(self, pk):
        movie = movie_service.read_one(pk)
        data = movie_schema.dump(movie)
        return data, 200

    @movies_ns.doc(description="Update movie by id")
    @movies_ns.expect(movie_entity_fields)
    def put(self, pk):
        data = request.json
        movie_service.update(pk, data)
        return {}, 201, {"location": f"/movies/{pk}"}

    @movies_ns.doc(description="Delete movie by id")
    def delete(self, pk):
        movie_service.delete(pk)
        return {}, 204
