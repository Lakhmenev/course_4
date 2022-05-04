from sqlalchemy.orm.scoping import scoped_session
import project.config
from project.dao.models import Genre


class GenreDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Genre).filter(Genre.id == pk).one_or_none()

    def get_all(self, data_filter):
        genres = self._db_session.query(Genre)

        # Обрабатываем пагинацию
        page = data_filter.get('page')

        if page is not None:
            page_int = int(data_filter.get('page'))
            genres = genres.paginate(page_int, project.config.BaseConfig.ITEMS_PER_PAGE, False)

            return genres.items
        else:
            return genres.all()

    def create(self, genre_d):
        self._db_session.add(Genre(**genre_d))
        self._db_session.commit()

    def delete(self, pk):
        genre = self.get_by_id(pk)
        self._db_session.delete(genre)
        self._db_session.commit()

    def update(self, genre_d):
        genre = self.get_by_id(genre_d.get("id"))
        genre.name = genre_d.get("name")

        self._db_session.add(genre)
        self._db_session.commit()
