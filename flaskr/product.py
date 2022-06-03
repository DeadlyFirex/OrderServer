from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.product import Product
from models.data import Data
from services.database import db_session
from services.config import Config
from services.utilities import Utilities

from datetime import datetime

config = Config().get_config()
product = Blueprint('product', __name__, url_prefix='/product')


@product.route("/all", methods=['GET'])
@jwt_required()
def get_all_products():
    """
    Return all current products.

    :return: JSON-form templating result format.
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

    return Utilities.return_result(200, f"Fetched {len(result)} products successfully", result)


@product.route("/<uuid>", methods=['GET'])
@jwt_required()
def get_product(uuid):
    """
    Retrieves one single product based on UUID.

    :return: JSON in result template.
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

    return Utilities.return_result(200, "Fetched product successfully", local_product)


@product.route("/last_changed", methods=['GET'])
@jwt_required()
def get_products_last_changed():
    """
    Retrieves last changed timestamp and hash, indicating changes if different

    :return: JSON in result template.
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

    data = Data.query.first()

    return Utilities.return_result(200, "Successfully fetched product last changed",
                                   {"products_hash": data.products_hash,
                                    "products_last_changed": data.products_last_changed})
