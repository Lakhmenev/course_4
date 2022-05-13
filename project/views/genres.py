from flask_restx import abort, Namespace, Resource
from flask import request
from project.exceptions import ItemNotFound
from project.services import GenresService
from project.setup_db import db
from project.tools.utils import admin_access_required, auth_required

genres_ns = Namespace("genres")


@genres_ns.route("/")
class GenresView(Resource):
    @genres_ns.response(200, "OK")
    # @auth_required
    def get(self):
        data_filter = request.args
        return GenresService(db.session).get_all_genres(data_filter)

    @genres_ns.response(201, "OK")
    @admin_access_required
    def post(self):
        req_json = request.json
        GenresService(db.session).create(req_json)
        return [], 201


@genres_ns.route("/<int:genre_id>/")
class GenreView(Resource):
    @genres_ns.response(200, "OK")
    @genres_ns.response(404, "Genre not found")
    # @auth_required
    def get(self, genre_id: int):
        """
        Получить наименования жанра по его id
        ---
        tags:
        - id: "_"
            description: "ID genre"
        parameters:
          - in: path
                id: id
                type: int
                required: true

        responses:
          200:
            description: A single genre item

            schema:
              id: Genre
              properties:
                name:
                  type: string
                  description: The name of the genre
                  default: -
        """
        try:
            return GenresService(db.session).get_item_by_id(genre_id)
        except ItemNotFound:
            abort(404, message="Genre not found")

    @genres_ns.response(204, "Delete")
    @auth_required
    def delete(self, genre_id):
        """
        Удалить жанр по его id
        ---
        tags:
        - name: "genre"
            description: "Name genre"
        parameters:
          - in: path
                name: name
                type: string
                required: true

        responses:
          204:
            description:
        """
        GenresService(db.session).delete(genre_id)
        return [], 204

    @admin_access_required
    def put(self, genre_id):
        req_json = request.json
        req_json['id'] = genre_id
        GenresService(db.session).update(req_json)
        return [], 204

    @admin_access_required
    def patch(self, genre_id):
        req_json = request.json
        req_json['id'] = genre_id
        GenresService(db.session).update(req_json)
        return [], 204
