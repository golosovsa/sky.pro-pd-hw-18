"""
    Movies restX namespace

"""

from flask_restx import Namespace, Resource

movies_ns = Namespace("movies")


@movies_ns.route("/")
class MoviesView(Resource):

    def get(self):
        return {"message": "GET all movies route", "response": []}, 200

    def post(self):
        return {"message": "POST new movie route"}, 201, {"location": "/movies/<id>"}


@movies_ns.route("/<int:pk>")
class MovieView(Resource):

    def get(self, pk):
        return {"message": f"GET one movies route with id={pk}", "response": {}}, 200

    def put(self, pk):
        return {"message": f"PUT update movie route with id={pk}"}, 201, {"location": f"/movies/{pk}"}

    def delete(self, pk):
        return {"message": f"DELETE movie route with id={pk}"}, 200  # 204
