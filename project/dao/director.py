from sqlalchemy.orm.scoping import scoped_session
import project.config
from project.dao.models import Director


class DirectorDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Director).filter(Director.id == pk).one_or_none()

    def get_all(self, data_filter):
        directors = self._db_session.query(Director)

        # Обрабатываем пагинацию
        page = data_filter.get('page')

        if page is not None:
            page_int = int(data_filter.get('page'))
            directors = directors.paginate(page_int, project.config.BaseConfig.ITEMS_PER_PAGE, False)

            return directors.items
        else:
            return directors.all()

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
