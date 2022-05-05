from flask_restx import abort
from project.dao import AuthDAO
from project.services.base import BaseService
from project.tools.security import get_hash, generate_tokens
from project.tools.utils import decode_token


class AuthService(BaseService):
    def login(self, data: dict):
        user_data = AuthDAO(self._db_session).get_by_email(data['email'])

        if user_data is None:
            abort(401, message='Email not found')

        hash_password = get_hash(data['password'])

        if user_data['password'] != hash_password:
            return abort(401, message='Invalid password')

        tokens: dict = generate_tokens(
            {
                'email': data['email'],
                'role': user_data['role']
            },
        )
        return tokens

    def get_new_tokens(self, refresh_token: str):

        decoded_token = decode_token(refresh_token, refresh_token=True)

        tokens = generate_tokens(
            data={
                'email': decoded_token['email'],
                'role': decoded_token['role'],
            },
        )
        return tokens
