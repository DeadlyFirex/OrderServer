from flask import Blueprint
from flask_jwt_extended import jwt_required

from models.user import User
from services import config
from services.database import db_session
from services.utilities import Utilities, admin_required

config = config.Config().get_config()
user = Blueprint('user', __name__, url_prefix='/user')


@user.route("/<uuid>", methods=['GET'])
@jwt_required()
def get_user(uuid):
    """
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """
    if not Utilities.is_valid_uuid(uuid):
        return Utilities.return_bad_request()

    local_user = User.query.filter_by(uuid=uuid).first()

    if local_user is None:
        return Utilities.return_not_found()

    return Utilities.generate_public_user_payload(local_user)


@user.route("/all", methods=['GET'])
@jwt_required()
def get_all_users():
    """
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """

    local_users = User.query.all()

    if local_users is None or []:
        return Utilities.return_not_found()

    result = []

    for local_user in local_users:
        result.append(Utilities.generate_public_user_payload(local_user, code=None))

    return {"result": result}


@user.route("/admin/<uuid>", methods=['GET'])
@admin_required()
def get_admin_user(uuid):
    """
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """
    if not Utilities.is_valid_uuid(uuid):
        return Utilities.return_bad_request()

    local_user = User.query.filter_by(uuid=uuid).first()

    if local_user is None:
        return Utilities.return_not_found()

    return Utilities.generate_public_user_payload(local_user)


@user.route("/admin/delete/<uuid>", methods=['GET'])
@admin_required()
def delete_admin_user(uuid):
    """
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """
    if not Utilities.is_valid_uuid(uuid):
        return Utilities.return_bad_request()

    local_user = User.query.filter_by(uuid=uuid).first()

    if local_user is None:
        return Utilities.return_not_found()

    local_user.delete()
    db_session.commit()

    return Utilities.return_success()


@user.route("/admin/edit/<uuid>", methods=['PUT'])
@admin_required()
def put_admin_user(uuid):
    """
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """
    # Not implemented

    return Utilities.return_bad_request()


@user.route("/admin/create/<uuid>", methods=['POST'])
@admin_required()
def put_admin_new_user(uuid):
    """
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """
    # Not implemented

    return Utilities.return_bad_request()
