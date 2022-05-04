from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.tools.security import generate_password_digest


class UsersService(BaseService):
    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self, data_filter):
        users = UserDAO(self._db_session)
        return UserSchema(many=True).dump(users.get_all(data_filter))

    def create(self, user_d):
        user_d['password'] = generate_password_digest(user_d['password'])
        return UserDAO(self._db_session).create(user_d)

    def update(self, user_d):
        return UserDAO(self._db_session).update(user_d)

    def delete(self, pk):
        return UserDAO(self._db_session).delete(pk)
