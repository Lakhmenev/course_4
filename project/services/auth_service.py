from project.dao.auth import AuthDAO
from project.tools.security import generate_password_digest, get_hash, generate_tokens
from project.tools.util import decode_token


class AuthService:

    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def login(self, email, password, role):
        hash_password = generate_password_digest(password)

        # hash_password_old = get_hash(password)

        if password == hash_password:
            tokens: dict = generate_tokens(
                {
                    'email': email,
                    'role': role,
                },
            )
            return tokens

    def get_new_tokens(self, refresh_token: str):

        decoded_token = decode_token(refresh_token, refresh_token=True)

        tokens = generate_tokens(
            data={
                'username': decoded_token['username'],
                'role': decoded_token['role'],
            },
        )
        return tokens
