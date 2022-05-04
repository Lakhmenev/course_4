from flask_restx import abort, Namespace, Resource
from flask import request
from project.exceptions import ItemNotFound
from project.services import UsersService
from project.setup_db import db

users_ns = Namespace("users")


@users_ns.route("/")
class UsersView(Resource):
    @users_ns.response(200, "OK")
    def get(self):
        """Get all users"""
        return UsersService(db.session).get_all_users()

    @users_ns.response(201, "OK")
    def post(self):
        req_json = request.json
        UsersService(db.session).create(req_json)
        return [], 201


@users_ns.route("/<int:user_id>")
class UserView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def get(self, user_id: int):
        """Get user by id"""
        try:
            return UsersService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User not found")

    def delete(self, user_id):
        UsersService(db.session).delete(user_id)
        return [], 204

    def put(self, user_id):
        req_json = request.json
        req_json['id'] = user_id
        UsersService(db.session).update(req_json)
        return [], 204

    def patch(self, user_id):
        req_json = request.json
        req_json['id'] = user_id
        UsersService(db.session).update(req_json)
        return [], 204
