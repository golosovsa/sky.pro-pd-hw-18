"""
    Genres restX namespace

"""

from flask import jsonify
from flask_restx import Namespace, Resource

genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):

    def get(self):
        return jsonify({"message": "GET all genres route", "response": []}), 200


@genres_ns.route("/<int:pk>")
class GenreView(Resource):

    def get(self, pk):
        return jsonify({"message": f"GET one genre route with id={pk}", "response": {}}), 200

