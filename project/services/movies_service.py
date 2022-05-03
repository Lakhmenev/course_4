from project.dao import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema
from project.services.base import BaseService


class MoviesService(BaseService):
    def get_item_by_id(self, pk):
        movie = MovieDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self, data_filter):
        movies = MovieDAO(self._db_session)
        return MovieSchema(many=True).dump(movies.get_all(data_filter))

    def create(self, genre_d):
        return MovieDAO(self._db_session).create(genre_d)

    def update(self, genre_d):
        return MovieDAO(self._db_session).update(genre_d)

    def delete(self, pk):
        return MovieDAO(self._db_session).delete(pk)
