from project.setup_db import db


favorites = db.Table(
    'favorite',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('movie_id', db.Integer(), db.ForeignKey('movie.id'))
)
