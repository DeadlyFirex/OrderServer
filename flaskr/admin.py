from datetime import datetime
from uuid import uuid4

from bcrypt import hashpw, gensalt
from sqlalchemy.exc import IntegrityError

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from models.data import Data
from models.product import Product
from models.user import User
from services.database import db_session
from services.utilities import Utilities as utils, admin_required

# Configure blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route("/product/populate", methods=['GET'])
@admin_required()
def get_admin_product_populate():
    """
    Populate all products in the database.\n
    This is retrieved from the ``products.json``.

    :return: JSON status response.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    # Perform tracking
    if current_user is None:
        return utils.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    # Track time taken
    start_time = datetime.now()

    # Load in file
    from json import load
    result = load(open("./static/products.json"))["products"]

    # Remove old entries
    db_session.query(Product).delete()

    count = 0
    for product in result:
        count += 1
        # TODO: Improve this to automatic decoding/mapping
        new_product = Product(id=product["id"], uuid=str(uuid4()), name=product["name"], brand=product["brand"],
                              price=product["price"], category=product["category"], description=product["description"],
                              image=product["image"], image_path=product["image_path"],
                              original_link=product["original_link"],

                              nutri_score=product["nutri_score"].upper(), quantity=product["quantity"],
                              allergens=product["allergens"], ingredients=product["ingredients"],

                              energy=product["energy"], fat=product["fat"], saturated_fat=product["saturated_fat"],
                              unsaturated_fat=product["unsaturated_fat"], carbohydrates=product["carbohydrates"],
                              sugars=product["sugars"], fiber=product["fiber"], proteins=product["proteins"],
                              salt=product["salt"], extra=product["extra"])
        db_session.add(new_product)
    db_session.commit()

    # Rehash and re-stamp
    Data.query.first().perform_changes("products")

    time = utils.calculate_time(start_time)
    return utils.detailed_response(200, f"Successfully repopulated {count} products in {time}ms",
                                   {"count": count,
                                    "time": f"{time}ms"
                                    })


@admin.route("/user/add", methods=['POST'])
@admin_required()
def post_admin_user_add():
    """
    Add a user, handling an HTTP POST request. \n
    This creates and adds a user to the database, if valid.

    :return: JSON status response.
    """

    try:
        username: str = request.json.get("username", None)
        name: str = request.json.get("name", None)
        email: str = request.json.get("email", None)
        phone_number: str = request.json.get("phone_number", None)
        postal_code: str = request.json.get("postal_code", None)
        address: str = request.json.get("address", None)

        if not all(isinstance(i, str) for i in [username, name, email, phone_number, postal_code, address]):
            raise ValueError(
                f"Expected str, instead got [{type(username), type(name), type(email), type(phone_number), type(postal_code), type(address)}]")

    except (AttributeError, ValueError) as e:
        return utils.detailed_response(400, "Bad request, see details.", {"error": e.__str__()})

    raw_password = utils.generate_secret()

    try:
        new_user = User(
            name=name,
            username=username,
            email=utils.validate_email(email) or "invalid@email.com",
            admin=False,
            password=hashpw(raw_password.encode("UTF-8"), gensalt()).decode("UTF-8"),
            address=address,
            phone_number=utils.validate_phone(phone_number) or "0612345678",
            postal_code=utils.validate_postalcode(postal_code) or "1234AB"
        )

        db_session.add(new_user)
        db_session.commit()

    except IntegrityError as error:
        return utils.custom_response(400, f"Bad request, check details for more info",
                                     {"error": error.args[0],
                                      "constraint": error.args[0].split(":")[1].removeprefix(" ")})

    return utils.custom_response(201, f"Successfully created user {new_user.username}",
                                 {"login": {"uuid": new_user.uuid, "password": raw_password}})


@admin.route("/user/delete/<uuid>", methods=['DELETE'])
@admin_required()
def post_admin_user_delete(uuid: str):
    """
    Deletes a user, handling an HTTP DELETE request.\n
    This deletes a user based on UUID, if they exist.

    :return: JSON status response.
    """

    if not utils.validate_uuid(uuid):
        return utils.response(400, "Bad request, given value is not a UUID.")

    count = User.query.filter_by(uuid=uuid).delete()

    if count < 1:
        return utils.response(404, f"User <{uuid}> not found, unable to delete.")

    db_session.commit()
    return utils.detailed_response(200, f"Successfully deleted {count} user", {"uuid": uuid})


@admin.route("/product/add", methods=['POST'])
@admin_required()
def post_admin_product_add():
    """
    Placeholder. New products should be added through product.json.

    :return: JSON status response.
    """
    return utils.response(301, "Unsupported, instead, check /admin/product/populate")


@admin.route("/product/delete/<uuid>", methods=['DELETE'])
@admin_required()
def post_admin_product_delete(uuid: str):
    """
    Deletes a product, handling an HTTP DELETE request.\n
    This deletes a product based on UUID, if they exist.

    :return: JSON status response.
    """

    if not utils.validate_uuid(uuid):
        return utils.response(400, "Bad request, given value is not a UUID.")

    count = Product.query.filter_by(uuid=uuid).delete()

    if count < 1:
        return utils.response(404, f"Product <{uuid}> not found, unable to delete.")

    db_session.commit()
    return utils.detailed_response(200, f"Successfully deleted {count} product", {"uuid": uuid})

# @admin.route("/user/<uuid>", methods=['GET'])
# @admin_required()
# def get_admin_user(uuid):
#     """
#     Simply checks the connection status and if the application exists.
#
#     :return: JSON-form representing aliveness?
#     """
#     if not utils.is_valid_uuid(uuid):
#         return utils.return_response(400, "Expected UUID, received something else.")
#
#     local_user = User.query.filter_by(uuid=uuid).first()
#
#     if local_user is None:
#         return utils.return_response(404, f"User <{uuid}> not found.")
#
#     return utils.generate_public_user_payload(local_user)
