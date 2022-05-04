from project.dao import GenreDAO
from project.exceptions import ItemNotFound
from project.schemas.genre import GenreSchema
from project.services.base import BaseService


class GenresService(BaseService):
    def get_item_by_id(self, pk):
        genre = GenreDAO(self._db_session).get_by_id(pk)
        if not genre:
            raise ItemNotFound
        return GenreSchema().dump(genre)

    def get_all_genres(self, data_filter):
        genres = GenreDAO(self._db_session)
        return GenreSchema(many=True).dump(genres.get_all(data_filter))

    def create(self, genre_d):
        return GenreDAO(self._db_session).create(genre_d)

    def update(self, genre_d):
        return GenreDAO(self._db_session).update(genre_d)

    def delete(self, pk):
        return GenreDAO(self._db_session).delete(pk)
