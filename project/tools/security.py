import hashlib
import base64
from datetime import datetime, timedelta
import jwt
from project import constants


# Метод хеширование пароля 1
def generate_password_digest(password):
    return base64.b64encode(
        hashlib.pbkdf2_hmac(
            hash_name=constants.PWD_HASH_NAME,
            password=password.encode("utf-8"),
            salt=constants.PWD_HASH_SALT,
            iterations=constants.PWD_HASH_ITERATIONS,
        )).decode('utf-8')


# Метод хеширование пароля 2
def get_hash(password):
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name=constants.PWD_HASH_NAME,
        password=password.encode('utf-8'),
        # salt=constants.PWD_HASH_SALT_FOR_GET_HASH.encode('utf-8'),
        salt=constants.PWD_HASH_SALT,
        iterations=constants.PWD_HASH_ITERATIONS,
    )
    return base64.b64encode(hashed_password).decode('utf-8')


# Метод получения токенов
def generate_tokens(data: dict):
    data['exp'] = datetime.utcnow() + timedelta(minutes=constants.TOKEN_EXPIRE_MINUTES)
    data['refresh_token'] = False

    access_token = jwt.encode(
        payload=data,
        key=constants.SECRET_KEY,
        algorithm=constants.PWD_HASH_ALGORITHM,
    )

    data['exp'] = datetime.utcnow() + timedelta(days=constants.TOKEN_EXPIRE_DAYS)
    data['refresh_token'] = True

    refresh_token: str = jwt.encode(
        payload=data,
        key=constants.SECRET_KEY,
        algorithm=constants.PWD_HASH_ALGORITHM,
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
