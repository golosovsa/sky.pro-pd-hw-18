"""
    Directors restX namespace

"""

from flask_restx import Namespace, Resource, fields

from app.dao.model.director import DirectorSchema
from app.service_container import director_service

directors_ns = Namespace("directors", description="API route for director entities")

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

director_entity_fields = directors_ns.model("Director Entity", {
    "name": fields.String(),
})


@directors_ns.doc(model=director_entity_fields)
@directors_ns.route("/")
class DirectorsView(Resource):

    @directors_ns.doc(description="Get all directors")
    def get(self):
        data = director_service.read_all()
        return directors_schema.dump(data), 200


@directors_ns.route("/<int:pk>")
class DirectorView(Resource):

    @directors_ns.doc(description="Get director by id")
    def get(self, pk):
        data = director_service.read_one(pk)
        return director_schema.dump(data), 200
