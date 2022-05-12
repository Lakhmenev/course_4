from flask import Flask, render_template
from flask_cors import CORS
from flask_restx import Api, Resource


from project.setup_db import db
from project.views import auth_ns
from project.views import directors_ns
from project.views import genres_ns
from project.views import movies_ns
from project.views import protected_ns
from project.views import user_ns
from project.views import users_ns
from project.views import favorites_ns


api = Api(
    authorizations={
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    title="Flask Course Project 3",
    doc="/docs",
)

# Нужно для работы с фронтендом
cors = CORS()


class Username(Resource):
    def get(self, username):
        """
        This examples uses FlaskRESTful Resource
        It works also with swag_from, schemas and spec_dict
        ---
        parameters:
          - in: path
            name: username
            type: string
            required: true

        responses:
          200:
            description: A single user item

            schema:
              id: User
              properties:

                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        return {'username': username}, 200


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route('/')
    def index():
        return render_template('index.html')

    cors.init_app(app)
    db.init_app(app)
    api.init_app(app)

    # Регистрация эндпоинтов
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(users_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(protected_ns)
    api.add_namespace(favorites_ns)

    api.add_resource(Username, '/username/<username>')

    return app
