from sqlalchemy.orm.scoping import scoped_session

from project.dao.models import Director


class DirectorDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Director).filter(Director.id == pk).one_or_none()

    def get_all(self):
        return self._db_session.query(Director).all()

    def create(self, director_d):
        self._db_session.add(Director(**director_d))
        self._db_session.commit()

    def delete(self, pk):
        director = self.get_by_id(pk)
        self._db_session.delete(director)
        self._db_session.commit()

    def update(self, director_d):
        director = self.get_by_id(director_d.get("id"))
        director.name = director_d.get("name")

        self._db_session.add(director)
        self._db_session.commit()
