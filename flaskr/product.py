from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.product import Product
from models.data import Data
from services.utilities import Utilities

# Configure blueprint
product = Blueprint('product', __name__, url_prefix='/product')


@product.route("/all", methods=['GET'])
@jwt_required()
def get_product_all():
    """
    Return all current products.

    :return: JSON result response with a (list of product) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    local_products = Product.query.all()

    if local_products is None or local_products == []:
        return Utilities.response(404, "No products found")

    result = []

    for local_product in local_products:
        result.append(local_product)

    return Utilities.return_result(200, f"Fetched {len(result)} products successfully", result)


@product.route("/<uuid>", methods=['GET'])
@jwt_required()
def get_product_by_uuid(uuid):
    """
    Retrieves one single product based on uuid.

    :return: JSON result response with (product) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    local_product = Product.query.filter_by(uuid=uuid).first() or None

    if local_product is None:
        return Utilities.response(404, f"Product <{uuid}> not found")

    return Utilities.return_result(200, "Fetched product successfully", local_product)


@product.route("/last_changed", methods=['GET'])
@jwt_required()
def get_products_last_changed():
    """
    Retrieves last changed timestamp and hash, indicating changes if different.

    :return: JSON result response with (last changed) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    data = Data.query.first()

    return Utilities.return_result(200, "Successfully fetched product last changed",
                                   {"products_hash": data.products_hash,
                                    "products_last_changed": data.products_last_changed})
