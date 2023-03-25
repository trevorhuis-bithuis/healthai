from flask import Flask

from src.chats.chats import chats_blueprint
from src.users.users import users_blueprint
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(script_info=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    app.register_blueprint(users_blueprint)
    app.register_blueprint(chats_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
