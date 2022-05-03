from sqlalchemy.orm.scoping import scoped_session
# from models.base import BaseMixin
from project.dao.models import Movie


class MovieDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(Movie).filter(Movie.id == pk).one_or_none()

    def get_all(self):
        return self._db_session.query(Movie).all()

    def create(self, movie_d):
        # ent = Movie(**movie_d)
        movie = {}

        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self._db_session.add(movie)
        self._db_session.commit()
        return movie

    def delete(self, pk):
        movie = self.get_by_id(pk)
        self._db_session.delete(movie)
        self._db_session.commit()

    def update(self, movie_d):
        movie = self.get_by_id(movie_d.get("id"))

        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self._db_session.add(movie)
        self._db_session.commit()
