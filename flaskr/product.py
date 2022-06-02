from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.database import db_session
from models.user import User
from models.product import Product
from services.config import Config
from services.utilities import Utilities, admin_required

from datetime import datetime

config = Config().get_config()
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
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_ALL_PRODUCTS"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    local_products = Product.query.all()

    if local_products is None or local_products == []:
        return Utilities.return_response(404, "No products found")

    result = []

    for local_product in local_products:
        result.append(local_product)

    return {"status": 200, "message": f"Fetched {len(result)} products successfully", "result": result}, 200


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
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_PRODUCT"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    local_product = Product.query.filter_by(uuid=uuid).first() or None

    if local_product is None:
        return Utilities.return_response(404, f"Product <{uuid}> not found")

    return {"status": 200, "message": "Fetched product successfully", "result": local_product}, 200


@product.route("/last_changed", methods=['GET'])
@jwt_required()
def get_products_last_changed():
    """
    TODO: Update this docstring
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_PRODUCTS_LAST_CHANGED"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    # TODO: Implement this

    return Utilities.return_response(200, "This is a message")


@product.route("/<uuid>/last_changed", methods=['GET'])
@jwt_required()
def get_product_last_changed(uuid):
    """
    TODO: Update this docstring
    Simply checks the connection status and if the application exists.

    :return: JSON-form representing aliveness?
    """

    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_PRODUCT_LAST_CHANGED"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    # TODO: Implement this

    return Utilities.return_response(200, "This is a message")

