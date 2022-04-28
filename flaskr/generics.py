from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity

from services import config

config = config.Config().get_config()
generics = Blueprint('generics', __name__, url_prefix='/')


@generics.route("/health", methods=['GET'])
def get_health():
    """
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """

    return {"status": 200, "health": "ok"}, 200


@generics.route("/version", methods=['GET'])
def get_version():
    """
    Gets the current running version from the configuration, and uses it.

    :return: JSON-form representing version prefix
    """

    return {"status": 301, "link": config.server.version}, 301
