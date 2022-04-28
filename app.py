from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager

from flaskr import auth, generics, user
from services.config import Config
from services.database import db_session, init_db
from services.utilities import Utilities

from datetime import datetime
from os import path

# Get configuration, create Flask application
config = Config().get_config()


def create_app():
    app = Flask(config.application.name)
    jwt = JWTManager(app)

    # Setup configuration
    app.config.from_mapping(
        DEBUG=config.application.debug,
        SECRET_KEY=Utilities.generate_secret(),
        DATABASE=path.join(app.instance_path, config.database.filename),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{config.database.absolute_path}",
        JWT_SECRET_KEY=Utilities.generate_secret(),
    )

    # Configure blueprints/views and ratelimiting
    limiter = Limiter(app, key_func=get_remote_address, default_limits=[config.ratelimiting.default])
    limiter.limit(config.ratelimiting.default)(generics.generics)
    limiter.limit(config.ratelimiting.default)(auth.auth)
    limiter.limit(config.ratelimiting.default)(user.user)

    app.register_blueprint(generics.generics)
    app.register_blueprint(auth.auth)
    app.register_blueprint(user.user)

    return app


# @app.before_first_request
# def create_user():
#     init_db()
#     db_session.add(name="Deadly", last_name="Alden", email="deadly@gmail.com",
#                              created_at=datetime.now(), rank="", admin=True, password="ello")
#     db_session.commit()


if __name__ == "__main__":
    create_app().run(config.server.host, config.server.port, config.server.debug)
