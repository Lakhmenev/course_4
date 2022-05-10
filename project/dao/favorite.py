from sqlalchemy.orm.scoping import scoped_session
from project.dao.models import favorites


class FavoriteDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def create(self, favorite_d):
        add_favorite = favorites.insert().values(
            user_id=favorite_d['user_id'], movie_id=favorite_d['movie_id']
        )

        self._db_session.execute(add_favorite)
        self._db_session.commit()

    def delete(self, favorite_d):
        del_favorite = favorites.delete(user_id=favorite_d['user_id'], movie_id=favorite_d['movie_id'])

        print(del_favorite)
        # delete(user_id=favorite_d['user_id'], movie_id=favorite_d['movie_id'])

        self._db_session.delete(del_favorite)
        self._db_session.commit()
