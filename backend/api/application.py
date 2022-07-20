import toml
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from api.config.read import CONFIG
from api.persistence.tables import SESSION_FACTORY


def create_application() -> Flask:
    """Factory function for bootstrapping Flask application"""
    app = Flask(__name__)
    app.config.from_mapping(CONFIG)
    api = Api(app)

    CORS(app)

    @app.route("/health")
    def hello_world():
        return "OK"

    session = SESSION_FACTORY()
    session.begin()
    session.close()

    return app


if __name__ == "__main__":
    create_application().run(port=5000)
