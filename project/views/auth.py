from flask_restx import Resource, Namespace
from project.services import AuthService
from flask import request

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        reg_json = request.json
        email = reg_json.get(['email'], None)
        password = reg_json.get(['password'], None)
        role = reg_json.get(['role'], None)

        if None in ['email', 'password', 'role']:
            return "", 400

        tokens = AuthService.login(email, password, role)

        return tokens, 201

    def put(self):
        pass
        # return AuthService.get_new_tokens(request.json['refresh_token'])


