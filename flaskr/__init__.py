from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import OperationalError

from flaskr import admin, auth, generics, order, product, user, event
from models.data import Data
from models.user import User
from models.event import Event
from services.config import Config
from services.database import init_db
from services.utilities import Utilities

from os import path, system as os_system

# Get configuration, create Flask application
config = Config().get_config()


def create_app():
    app = Flask(config.application.name)

    # Set host configuration
    os_system(f"set FLASK_RUN_HOST={config.server.host}")
    os_system(f"set FLASK_RUN_PORT={config.server.port}")

    # Setup configuration
    app.config.from_mapping(
        DEBUG=config.application.debug,
        SECRET_KEY=Utilities.generate_secret(),
        DATABASE=path.join(app.instance_path, config.database.filename),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{config.database.absolute_path}",
        JWT_SECRET_KEY=Utilities.generate_secret(),
    )

    # Configure blueprints/views and ratelimiting
    # TODO: Make every limit configurable
    limiter = Limiter(app, key_func=get_remote_address, default_limits=[config.ratelimiting.default])
    limiter.limit(config.ratelimiting.default)(admin.admin)
    limiter.limit(config.ratelimiting.authorization)(auth.auth)
    limiter.limit(config.ratelimiting.default)(generics.generics)
    limiter.limit(config.ratelimiting.default)(order.order)
    limiter.limit(config.ratelimiting.default)(product.product)
    limiter.limit(config.ratelimiting.default)(user.user)
    limiter.limit(config.ratelimiting.default)(event.event)

    app.register_blueprint(admin.admin)
    app.register_blueprint(auth.auth)
    app.register_blueprint(generics.generics)
    app.register_blueprint(order.order)
    app.register_blueprint(product.product)
    app.register_blueprint(user.user)
    app.register_blueprint(event.event)

    # Register JWT
    jwt = JWTManager(app).init_app(app)

    # Check database status
    # TODO: Improve this function to be more flexible.
    @app.before_first_request
    def first_time_run():
        app.logger.info("Checking for database initialization.")
        try:
            result = (User.query.all(), Event.query.all(), Data.query.all())
        except OperationalError:
            init_db()
            app.logger.info("Performing new database initialization.")
            return
        if None in result or [] in result:
            init_db()
            app.logger.info("Repopulating database tables.")
            return
        app.logger.info("Finished checking, no new initialization required.")

    return app


if __name__ == "__main__":
    create_app().run(config.server.host, config.server.port, config.server.debug)
