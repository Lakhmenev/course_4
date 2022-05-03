from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    favorite_genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    role = db.Column(db.String(50), nullable=False)

    favorite_genre = db.relationship("Genre")

    def __repr__(self):
        return f"<User '{self.email, self.name, self.surname, self.role}'>"
