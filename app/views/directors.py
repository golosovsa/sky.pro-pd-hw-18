"""
    Directors restX namespace

"""

from flask_restx import Namespace, Resource

directors_ns = Namespace("directors")


@directors_ns.route("/")
class DirectorsView(Resource):

    def get(self):
        return {"message": "GET all directors route", "response": []}, 200


@directors_ns.route("/<int:pk>")
class DirectorView(Resource):

    def get(self, pk):
        return {"message": f"GET one director route with id={pk}", "response": {}}, 200

