import base64

PWD_HASH_SALT_FOR_GET_HASH = 'secret here'
PWD_HASH_NAME = 'sha256'
PWD_HASH_SALT = base64.b64decode("salt")
PWD_HASH_ITERATIONS = 100_000
PWD_HASH_ALGORITHM = 'HS256'