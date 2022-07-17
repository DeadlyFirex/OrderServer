from flask import Blueprint
from flask_jwt_extended import get_jwt_identity

from models.data import Data
from models.product import Product
from models.user import User
from services.utilities import Utilities, user_required

# Configure blueprint
product = Blueprint('product', __name__, url_prefix='/product')


@product.route("/all", methods=['GET'])
@user_required()
def get_product_all():
    """
    Return all current products.

    :return: JSON result response with a (list of product) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    local_products = Product.query.all()

    if local_products is None or local_products == []:
        return Utilities.response(404, "No products found")

    result = []

    for local_product in local_products:
        result.append(local_product)

    return Utilities.return_result(200, f"Fetched {len(result)} products successfully", result)


@product.route("/<uuid>", methods=['GET'])
@user_required()
def get_product_by_uuid(uuid):
    """
    Retrieves one single product based on uuid.

    :return: JSON result response with (product) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    local_product = Product.query.filter_by(uuid=uuid).first() or None

    if local_product is None:
        return Utilities.response(404, f"Product <{uuid}> not found")

    return Utilities.return_result(200, "Fetched product successfully", local_product)


@product.route("/last_changed", methods=['GET'])
@user_required()
def get_products_last_changed():
    """
    Retrieves last changed timestamp and hash, indicating changes if different.

    :return: JSON result response with (last changed) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    data = Data.query.first()

    return Utilities.return_result(200, "Successfully fetched product last changed",
                                   {"products_hash": data.products_hash,
                                    "products_last_changed": data.products_last_changed})
