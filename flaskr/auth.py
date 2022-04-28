from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from services.database import db_session
from models.user import User
from services import config
from services.utilities import Utilities, admin_required

from datetime import datetime

config = config.Config().get_config()
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/login", methods=['POST'])
def post_login():
    """
    TODO: Update this docstring
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """
    try:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
    except AttributeError:
        return Utilities.return_bad_request()

    user = User.query.filter_by(username=username, password=password).first()

    if user is None:
        return Utilities.return_unauthorized()

    lifetime = Utilities.generate_token_timedelta()
    user.token = create_access_token(identity=user.uuid, fresh=False, expires_delta=lifetime,
                                     additional_claims=Utilities.generate_user_payload(user))

    user.active = True
    user.login_count += 1
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr

    db_session.commit()

    return {"status": 200, "token": user.token, "lifetime": lifetime.total_seconds()}, 200


@auth.route("/test", methods=['GET'])
@jwt_required()
def get_test_login():
    """
    TODO: Update this docstring
    Simply checks if you're properly logged in

    :return: JSON-form
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_unauthorized()

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "TEST_LOGIN"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    return {"status": 200, "response": f"Logged in as {user.username}", "uuid": user.uuid}, 200


@auth.route("/admin/test", methods=['GET'])
@admin_required()
def get_admin_test_login():
    """
    TODO: Update this docstring
    Simply checks if you're properly logged in

    :return: JSON-form
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_unauthorized()

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "TEST_ADMIN_LOGIN"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    return {"status": 200, "response": f"Logged in as {user.username}", "uuid": user.uuid, "admin": True}, 200
