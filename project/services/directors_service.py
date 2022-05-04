from project.dao import DirectorDAO
from project.exceptions import ItemNotFound
from project.schemas.derector import DirectorSchema
from project.services.base import BaseService


class DirectorsService(BaseService):
    def get_item_by_id(self, pk):
        director = DirectorDAO(self._db_session).get_by_id(pk)
        if not director:
            raise ItemNotFound
        return DirectorSchema().dump(director)

    def get_all_directors(self, data_filter):
        directors = DirectorDAO(self._db_session)
        return DirectorSchema(many=True).dump(directors.get_all(data_filter))

    def create(self, director_d):
        return DirectorDAO(self._db_session).create(director_d)

    def update(self, director_d):
        return DirectorDAO(self._db_session).update(director_d)
    
    def delete(self, pk):
        return DirectorDAO(self._db_session).delete(pk)
