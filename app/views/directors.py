"""
    Directors restX namespace

"""

from flask_restx import Namespace, Resource

from app.dao.model.director import DirectorSchema
from app.service_container import director_service


directors_ns = Namespace("directors")

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route("/")
class DirectorsView(Resource):

    def get(self):
        data = director_service.read_all()
        return directors_schema.dump(data), 200


@directors_ns.route("/<int:pk>")
class DirectorView(Resource):

    def get(self, pk):
        data = director_service.read_one(pk)
        return director_schema.dump(data), 200

