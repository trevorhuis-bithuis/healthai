import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.diet.diet import diet_blueprint
from src.users.users import users_blueprint
from src.auth.auth import auth_blueprint
from src.exercise.exercise import exercise_blueprint

from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(script_info=None):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)
    CORS(app)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    app.register_blueprint(users_blueprint)
    app.register_blueprint(diet_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(exercise_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
