"""
    Movies restX namespace

"""

from flask_restx import Namespace, Resource
from flask import request

from app.dao.model.movie import MovieSchema
from app.service_container import movie_service


movies_ns = Namespace("movies")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route("/")
class MoviesView(Resource):

    def get(self):
        movie = movie_service.read_all()
        return movies_schema.dump(movie), 200

    def post(self):
        data = request.json
        movie = movie_service.create(data)
        return {}, 201, {"location": f"/movies/{movie.id}"}


@movies_ns.route("/<int:pk>")
class MovieView(Resource):

    def get(self, pk):
        return {"message": f"GET one movies route with id={pk}", "response": {}}, 200

    def put(self, pk):
        return {"message": f"PUT update movie route with id={pk}"}, 201, {"location": f"/movies/{pk}"}

    def delete(self, pk):
        return {"message": f"DELETE movie route with id={pk}"}, 200  # 204
