from sqlalchemy.orm.scoping import scoped_session
import project.config
from project.dao.models import Movie


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self, data_filter):
        movies = self._db_session.query(Movie)

        year = data_filter.get('year')

        if year is not None:
            movies = movies.filter(Movie.year == year)

        director_id = data_filter.get('director_id')

        if director_id is not None:
            movies = movies.filter(Movie.director_id == director_id)

        genre_id = data_filter.get('genre_id')

        if genre_id is not None:
            movies = movies.filter(Movie.genre_id == genre_id)

        # Обрабатываем если status=new
        status = data_filter.get('status')
        if status == 'new':
            movies = movies.order_by(Movie.id.desc())

        # Обрабатываем пагинацию
        page = data_filter.get('page')

        if page is not None:
            page_int = int(data_filter.get('page'))
            movies = movies.paginate(page_int, project.config.BaseConfig.ITEMS_PER_PAGE, False)

            return movies.items
        else:
            return movies.all()

    def create(self, movie_d):
        self._db_session.add(Movie(**movie_d))
        self._db_session.commit()

    def delete(self, pk):
        movie = self.get_by_id(pk)
        self._db_session.delete(movie)
        self._db_session.commit()

    def update(self, movie_d):
        movie = self.get_by_id(movie_d.get("id"))

        title = movie_d.get("title")
        if title is not None:
            movie.title = movie_d.get("title")

        description = movie_d.get("description")
        if description is not None:
            movie.description = movie_d.get("description")

        trailer = movie_d.get("trailer")
        if trailer is not None:
            movie.trailer = movie_d.get("trailer")

        year = movie_d.get("year")
        if year is not None:
            movie.year = movie_d.get("year")

        rating = movie_d.get("rating")
        if rating is not None:
            movie.rating = movie_d.get("rating")

        genre_id = movie_d.get("genre_id")
        if genre_id is not None:
            movie.genre_id = movie_d.get("genre_id")

        director_id = movie_d.get("director_id")
        if director_id is not None:
            movie.director_id = movie_d.get("director_id")

        self._db_session.add(movie)
        self._db_session.commit()
