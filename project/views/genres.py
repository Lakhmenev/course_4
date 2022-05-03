from flask_restx import abort, Namespace, Resource
from flask import request
from project.exceptions import ItemNotFound
from project.services import GenresService
from project.setup_db import db


genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):
    @genres_ns.response(200, "OK")
    def get(self):
        """Get all genres"""
        return GenresService(db.session).get_all_genres()

    @genres_ns.response(201, "OK")
    def post(self):
        req_json = request.json
        GenresService(db.session).create(req_json)
        return [], 201


@genres_ns.route("/<int:genre_id>")
class GenreView(Resource):
    @genres_ns.response(200, "OK")
    @genres_ns.response(404, "Genre not found")
    def get(self, genre_id: int):
        """Get genre by id"""
        try:
            return GenresService(db.session).get_item_by_id(genre_id)
        except ItemNotFound:
            abort(404, message="Genre not found")

    def delete(self, genre_id):
        GenresService(db.session).delete(genre_id)
        return [], 204

    def put(self, genre_id):
        req_json = request.json
        req_json['id'] = genre_id
        GenresService(db.session).update(req_json)
        return [], 204

    def patch(self, genre_id):
        req_json = request.json
        req_json['id'] = genre_id
        GenresService(db.session).update(req_json)
        return [], 204
