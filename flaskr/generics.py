from flask import Blueprint

from models.data import Data
from services.config import Config
from services.utilities import Utilities

config = Config().get_config()
generics = Blueprint('generics', __name__, url_prefix='/')


@generics.route("/health", methods=['GET'])
def get_health():
    """
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """

    return Utilities.return_response(200, "ok")


@generics.route("/version", methods=['GET'])
def get_version():
    """
    Gets the current running version from the configuration, and uses it.

    :return: JSON-form representing version prefix
    """

    return Utilities.return_complex_response(301, "ok", {"link": config.server.version})


@generics.route("/last_changed", methods=['GET'])
def get_last_changed():
    """
    Retrieves last changed data and returns it.

    :return: JSON in result template, last_changed row from data.
    """

    return Utilities.return_result(200, "Fetched result successfully", Data.query.first())
