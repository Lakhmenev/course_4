from sqlalchemy.orm.scoping import scoped_session
from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_by_id(self, pk):
        return self._db_session.query(User).filter(User.id == pk).one_or_none()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, user_d):
        # user = (**user_d)
        user = {}
        user.email = user_d.get("email")
        user.password = user_d.get("password")
        user.name = user_d.get("name")
        user.surname = user_d.get("surname")
        user.favorite_genre_id = user_d.get("favorite_genre_id")
        user.role = user_d.get("role")

        self._db_session.add(user)
        self._db_session.commit()
        return user

    def delete(self, pk):
        user = self.get_by_id(pk)
        self._db_session.delete(user)
        self._db_session.commit()

    def update(self, user_d):
        user = self.get_by_id(user_d.get("id"))

        user.email = user_d.get("email")
        user.password = user_d.get("password")
        user.name = user_d.get("name")
        user.surname = user_d.get("surname")
        user.favorite_genre_id = user_d.get("favorite_genre_id")
        user.role = user_d.get("role")

        self._db_session.add(user)
        self._db_session.commit()
