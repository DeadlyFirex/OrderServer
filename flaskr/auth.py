from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models.user import User
from services.database import db_session
from services.utilities import Utilities, admin_required

from datetime import datetime


# Configure blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/login", methods=['POST'])
def post_login():
    """
    Logs a user in, returns a JWT token for authentication.

    :return: JSON with JWT token.
    """
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not isinstance(username, str):
            raise ValueError(f"Expected str, instead got {type(username)}")
        if not isinstance(password, str):
            raise ValueError(f"Expected str, instead got {type(password)}")

    except AttributeError as e:
        return Utilities.return_complex_response(400, "Bad request, see details.", {"error": e.__str__()})

    user = User.query.filter_by(username=username, password=password).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    lifetime = Utilities.generate_token_timedelta()
    user.token = create_access_token(identity=user.uuid, fresh=False, expires_delta=lifetime,
                                     additional_claims=Utilities.generate_user_payload(user))

    user.active = True
    user.login_count += 1
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr

    db_session.commit()

    return Utilities.return_custom_response(200, f"Successfully logged in as {user.username}",
                                            {"login": {"uuid": user.uuid,
                                                       "token": user.token,
                                                       "lifetime": lifetime.total_seconds()}})


@auth.route("/test", methods=['GET'])
@jwt_required()
def get_login():
    """
    Simply checks if you're properly logged in.

    :return: JSON-form
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "TEST_LOGIN"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    return Utilities.return_custom_response(200, f"Logged in as {user.username}", {"login": {"uuid": user.uuid}})


@auth.route("/admin/test", methods=['GET'])
@admin_required()
def get_admin_login():
    """
    Simply checks if you're properly logged in as an administrator.

    :return: JSON-form
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "TEST_ADMIN_LOGIN"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    return Utilities.return_custom_response(200, f"Logged in as {user.username}", {"login": {"uuid": user.uuid,
                                                                                             "admin": user.admin}})
