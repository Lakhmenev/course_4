import hashlib
import base64
from datetime import datetime, timedelta
import jwt
from project import constants
from flask import current_app


def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name=constants.PWD_HASH_NAME,
        password=password.encode("utf-8"),
        salt=constants.PWD_HASH_SALT,
        iterations=constants.PWD_HASH_ITERATIONS,
    )


# Метод хеширование пароля
def get_hash(password):
    hashed_password = hashlib.pbkdf2_hmac(
            hash_name=constants.PWD_HASH_NAME,
            password=password.encode('utf-8'),
            salt=constants.PWD_HASH_SALT_FOR_GET_HASH.encode('utf-8'),
            iterations=constants.PWD_HASH_ITERATIONS,
            )
    return base64.b64encode(hashed_password).decode('utf-8')


# Метод получения токенов
def generate_tokens(data: dict):
    data['exp'] = datetime.utcnow() + timedelta(minutes=current_app.config.TOKEN_EXPIRE_MINUTES)
    data['refresh_token'] = False

    access_token = jwt.encode(
        payload=data,
        key=current_app.config.SECRET_KEY,
        algorithm=current_app.config.PWD_HASH_ALGORITHM,
    )

    data['exp'] = datetime.utcnow() + timedelta(days=current_app.config.TOKEN_EXPIRE_DAYS)
    data['refresh_token'] = True

    refresh_token: str = jwt.encode(
        payload=data,
        key=current_app.config.SECRET_KEY,
        algorithm=current_app.config.PWD_HASH_ALGORITHM,
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
