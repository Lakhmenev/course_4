from flask_restx import abort, Namespace, Resource
from flask import request
from project.exceptions import ItemNotFound
from project.services import UsersService
from project.setup_db import db
from project.tools.utils import auth_required_user_data, auth_required, \
    auth_required_user_data_patch, auth_required_user_change_password, admin_access_required

users_ns = Namespace("users")
user_ns = Namespace("user")


@users_ns.route("/")
class UsersView(Resource):
    @users_ns.response(200, "OK")
    @admin_access_required
    def get(self):
        data_filter = request.args
        return UsersService(db.session).get_all_users(data_filter)

    @users_ns.response(201, "OK")
    @admin_access_required
    def post(self):
        req_json = request.json
        UsersService(db.session).create(req_json)
        return [], 201


@users_ns.route("/<int:user_id>/")
class UserView(Resource):
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    @admin_access_required
    def get(self, user_id: int):
        """Get user by id"""
        try:
            return UsersService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User not found")

    @admin_access_required
    def delete(self, user_id):
        UsersService(db.session).delete(user_id)
        return [], 204

    @admin_access_required
    def put(self, user_id):
        req_json = request.json
        req_json['id'] = user_id
        UsersService(db.session).update(req_json)
        return [], 204

    @admin_access_required
    def patch(self, user_id):
        req_json = request.json
        req_json['id'] = user_id
        UsersService(db.session).update(req_json)
        return [], 204


@user_ns.route("/")
class UserView(Resource):
    @auth_required_user_data
    def get(self):
        # Всю информацию по данным пользователя возвращает декоратор
        return

    @auth_required_user_data_patch
    def patch(self):
        req_json = request.json
        return req_json


@user_ns.route("/password/")
class UserPasswordEdit(Resource):
    @auth_required_user_change_password
    def put(self):
        req_json = request.json
        return req_json
