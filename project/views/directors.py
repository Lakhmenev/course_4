from flask_restx import abort, Namespace, Resource
from flask import request
from project.exceptions import ItemNotFound
from project.services import DirectorsService
from project.setup_db import db
from project.tools.utils import admin_access_required, auth_required

directors_ns = Namespace("directors")


@directors_ns.route("/")
class DirectorsView(Resource):
    @directors_ns.response(200, "OK")
    @auth_required
    def get(self):
        data_filter = request.args
        return DirectorsService(db.session).get_all_directors(data_filter)

    @directors_ns.response(201, "OK")
    @admin_access_required
    def post(self):
        req_json = request.json
        DirectorsService(db.session).create(req_json)
        return [], 201


@directors_ns.route("/<int:director_id>/")
class DirectorView(Resource):
    @directors_ns.response(200, "OK")
    @directors_ns.response(404, "Director not found")
    @auth_required
    def get(self, director_id: int):
        """Get director by id"""
        try:
            return DirectorsService(db.session).get_item_by_id(director_id)
        except ItemNotFound:
            abort(404, message="Director not found")

    @admin_access_required
    def delete(self, director_id):
        DirectorsService(db.session).delete(director_id)
        return [], 204

    @admin_access_required
    def put(self, director_id):
        req_json = request.json
        req_json['id'] = director_id
        DirectorsService(db.session).update(req_json)
        return [], 204

    @admin_access_required
    def patch(self, director_id):
        req_json = request.json
        req_json['id'] = director_id
        DirectorsService(db.session).update(req_json)
        return [], 204
