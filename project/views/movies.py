from flask_restx import abort, Namespace, Resource
from flask import request
from project.exceptions import ItemNotFound
from project.services import MoviesService
from project.setup_db import db

movies_ns = Namespace("movies")


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.response(200, "OK")
    def get(self):
        data_filter = request.args
        return MoviesService(db.session).get_all_movies(data_filter)

    @movies_ns.response(201, "OK")
    def post(self):
        reg_json = request.json
        MoviesService(db.session).create(reg_json)
        return [], 201


@movies_ns.route("/<int:movie_id>/")
class MovieView(Resource):
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Genre not found")
    def get(self, movie_id: int):
        """Get movie by id"""
        try:
            return MoviesService(db.session).get_item_by_id(movie_id)
        except ItemNotFound:
            abort(404, message="Movie not found")

    def delete(self, movie_id):
        MoviesService(db.session).delete(movie_id)
        return [], 204

    def put(self, movie_id):
        req_json = request.json
        req_json['id'] = movie_id
        MoviesService(db.session).update(req_json)
        return [], 204

    def patch(self, movie_id):
        req_json = request.json
        req_json['id'] = movie_id
        MoviesService(db.session).update(req_json)
        return [], 204
