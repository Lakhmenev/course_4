from project.dao import FavoriteDAO
from project.services.base import BaseService


class FavoritesService(BaseService):
    def create(self, data):
        return FavoriteDAO(self._db_session).create(data)

    def delete(self, data):
        return FavoriteDAO(self._db_session).delete(data)
