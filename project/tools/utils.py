import jwt
from flask import request, current_app
from project.constants import SECRET_KEY, PWD_HASH_ALGORITHM
from flask_restx import abort
from project.dao.auth import AuthDAO
from project.dao.user import UserDAO
from project.setup_db import db
from project.tools.security import get_hash


def get_token_from_headers(headers: dict):
    if 'Authorization' not in headers:
        abort(401)

    return headers['Authorization'].split(' ')[-1]


def decode_token(token: str, refresh_token: bool = False):
    decoded_token = {}
    try:
        decoded_token = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[PWD_HASH_ALGORITHM],
        )
    except jwt.PyJWTError:
        current_app.logger.info('Got wrong token "%s"', token)
        abort(401)

    # Проверяем, что это не  refresh_token
    if decoded_token['refresh_token'] != refresh_token:
        abort(400, message='Got wrong token type.')

    return decoded_token


def auth_required(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        # Проверяем, что email существует.
        if not AuthDAO(db.session).get_by_email(decoded_token['email']):
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def admin_access_required(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        if decoded_token['role'] != 'admin':
            abort(403)

        # Проверяем, что пользователь с таким email существует.
        if not AuthDAO(db.session).get_by_email(decoded_token['email']):
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def auth_required_user_data(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        # Проверяем, что email существует.
        if not AuthDAO(db.session).get_by_email(decoded_token['email']):
            abort(401)

        # Получаем по полю email информацию профиля
        result = UserDAO(db.session).get_by_email(decoded_token['email'])

        data = {
            'email': result.email,
            'name': result.name,
            'surname': result.surname,
            'favourite_genre': result.favorite_genre
        }
        return data

    return wrapper


def auth_required_user_data_patch(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        # Проверяем, что email существует.
        if not AuthDAO(db.session).get_by_email(decoded_token['email']):
            abort(401)

        result = UserDAO(db.session).get_by_email(decoded_token['email'])

        new_data = func(*args, **kwargs)

        data = {
            'id': result.id,
            'name': new_data["name"],
            'surname': new_data["surname"],
            'favorite_genre': new_data["favourite_genre"]
        }

        UserDAO(db.session).update(data)

        return [], 204

    return wrapper


def auth_required_user_change_password(func):
    def wrapper(*args, **kwargs):
        # Получаем заголовок с токеном из запроса.
        token = get_token_from_headers(request.headers)

        # Пытаемся раскодировать токен
        decoded_token = decode_token(token)

        # Проверяем, что email существует.
        if not AuthDAO(db.session).get_by_email(decoded_token['email']):
            abort(401)

        result = UserDAO(db.session).get_by_email(decoded_token['email'])

        current_password = result.password

        new_data_password = func(*args, **kwargs)

        temp_password = get_hash(new_data_password['old_password'])

        if current_password != temp_password:
            return abort(401)

        temp_password = get_hash(new_data_password['new_password'])

        data = {
            'id': result.id,
            'password': temp_password,
        }

        UserDAO(db.session).update(data)
        return [], 204

    return wrapper
