from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from services.utilities import Utilities

# Configure blueprint
user = Blueprint('user', __name__, url_prefix='/user')


@user.route("/<uuid>", methods=['GET'])
@jwt_required()
def get_user_by_uuid(uuid):
    """
    Gets a single user by UUID and returns public information about them.

    :return: JSON result response with (user) data.
    """
    if not Utilities.is_valid_uuid(uuid):
        return Utilities.return_response(400, "Expected UUID, received something else.")

    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.return_response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    argument_user = User.query.filter_by(uuid=uuid).first()

    if argument_user is None:
        return Utilities.return_response(404, f"User <{uuid}> not found.")

    return Utilities.return_result(200, "Fetched user successfully", {"uuid": argument_user.uuid,
                                                                      "name": argument_user.name,
                                                                      "username": argument_user.username,
                                                                      "country": argument_user.country,
                                                                      "admin": argument_user.admin,
                                                                      "tags": argument_user.tags,
                                                                      "active": argument_user.active})


@user.route("/all", methods=['GET'])
@jwt_required()
def get_user_all():
    """
    Get all users and returns public information about them.

    :return: JSON result response with a (list of users) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.return_response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    fetched_users = User.query.all()

    if fetched_users is None or []:
        return Utilities.return_response(404, "No users were found.")

    result = []

    for fetched_user in fetched_users:
        result.append({"uuid": fetched_user.uuid, "name": fetched_user.name, "username": fetched_user.username,
                       "country": fetched_user.country, "admin": fetched_user.admin, "tags": fetched_user.tags,
                       "active": fetched_user.active})

    return Utilities.return_result(200, f"Successfully fetched {len(result)} users", result)
