from flask_restx import abort, Namespace, Resource
from flask import request
from project.exceptions import ItemNotFound
from project.services import FavoritesService
from project.setup_db import db
from project.tools.utils import get_user_id

favorites_ns = Namespace("favorites")


@favorites_ns.route("/movies/<int:movie_id>/")
class FavoritesView(Resource):
    def post(self, movie_id):
        user_id = get_user_id()
        data = {'user_id': user_id,
                'movie_id': movie_id
                }
        if user_id is not None:
            FavoritesService(db.session).create(data)
            return [], 201
        return abort(401)

    def delete(self, movie_id):
        user_id = get_user_id()
        data = {'user_id': user_id,
                'movie_id': movie_id
                }
        if data['user_id'] is not None and data['movie_id'] is not None:
            FavoritesService(db.session).delete(data)
            return [], 204
        return abort(401)

