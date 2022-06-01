from flask import Blueprint

from services import config
from services.utilities import Utilities

config = config.Config().get_config()
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
