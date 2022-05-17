from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.database import db_session
from models.user import User
from models.product import Product
from services import config
from services.utilities import Utilities, admin_required

from datetime import datetime

config = config.Config().get_config()
product = Blueprint('product', __name__, url_prefix='/product')


@product.route("/all", methods=['GET'])
@jwt_required()
def get_all_products():
    """
    TODO: Update this docstring
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_unauthorized()

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_ALL_PRODUCTS"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    local_products = Product.query.all()

    if local_products is None or []:
        return Utilities.return_not_found()

    result = []

    for local_product in local_products:
        result.append(local_product)

    return {"result": result}, 200


@product.route("/<uuid>", methods=['GET'])
@jwt_required()
def get_product(uuid):
    """
    TODO: Update this docstring
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_unauthorized()

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_PRODUCT"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    local_products = Product.query.filter_by(uuid=uuid).first()

    if local_products is None or []:
        return Utilities.return_not_found()

    return {"result": local_products}, 200


@product.route("/last_changed", methods=['GET'])
@jwt_required()
def get_product_last_changed(uuid):
    """
    TODO: Update this docstring
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_unauthorized()

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_PRODUCT_LAST_CHANGED"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    # TODO: Implement this

    return Utilities.return_success()
