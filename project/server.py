from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from flask_restx import Api
import pathlib
from pathlib import Path

from project.setup_db import db
from project.views import auth_ns
from project.views import directors_ns
from project.views import genres_ns
from project.views import movies_ns
from project.views import protected_ns
from project.views import user_ns
from project.views import users_ns
from project.views import favorites_ns

from flask_swagger_ui import get_swaggerui_blueprint


api = Api(
    authorizations={
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
    # title="Flask Course Project 4",
    # doc="/docs/",
)

# Нужно для работы с фронтендом
cors = CORS()


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)


    SWAGGER_URL = '/swagger'  # URL for exposing Swagger UI (without trailing '/')
    # 'http://petstore.swagger.io/v2/swagger.json'
    API_URL = '/static/swagger.json'    #  f"{Path(pathlib.Path.cwd(), 'project', 'static', 'swagger.json')}"

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    @app.route('/')
    def index():
        return render_template('index.html')

    cors.init_app(app)
    db.init_app(app)
    api.init_app(app)

    app.register_blueprint(swaggerui_blueprint)

    # Регистрация эндпоинтов
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(users_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(protected_ns)
    api.add_namespace(favorites_ns)

    return app
