import pytest

from project.dao import MovieDAO
from project.dao.models import Movie


class TestMovieDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = MovieDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        m = Movie(title="В тылу врага",
                  description="военная тематика",
                  trailer="url_1",
                  year="2000",
                  rating="7",
                  genre_id=1,
                  director_id=1)
        db.session.add(m)
        db.session.commit()
        return m

    @pytest.fixture
    def movie_2(self, db):
        m = Movie(title="Операция Ы",
                  description="комедия",
                  trailer="url_2",
                  year="2002",
                  rating="9",
                  genre_id=2,
                  director_id=2)
        db.session.add(m)
        db.session.commit()
        return m

    def test_get_movie_by_id(self, movie_1):
        assert self.dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self):
        assert self.dao.get_by_id(1) is None

    def test_get_all_movies(self, movie_1, movie_2):
        data_filter = {'page': None}
        assert self.dao.get_all(data_filter) == [movie_1, movie_2]
