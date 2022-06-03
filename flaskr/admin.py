from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity

from models.user import User
from models.product import Product
from models.data import Data
from services.database import db_session
from services.utilities import Utilities, admin_required

from uuid import uuid4
from datetime import datetime

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
        return Utilities.return_response(401, "Unauthorized")
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
                              image=product["image"], image_path=product["image_path"], original_link=product["original_link"],

                              nutri_score=product["nutri_score"].upper(), quantity=product["quantity"],
                              allergens=product["allergens"], ingredients=product["ingredients"],

                              energy=product["energy"], fat=product["fat"], saturated_fat=product["saturated_fat"],
                              unsaturated_fat=product["unsaturated_fat"], carbohydrates=product["carbohydrates"],
                              sugars=product["sugars"], fiber=product["fiber"], proteins=product["proteins"],
                              salt=product["salt"], extra=product["extra"])
        db_session.add(new_product)
    db_session.commit()

    # Rehash and re-stamp
    Data.query.first().generate_changes("products")

    time = Utilities.calculate_time(start_time)
    return Utilities.return_complex_response(200, f"Successfully repopulated {count} products in {time}ms",
                                             {"count": count,
                                              "time": f"{time}ms"
                                              })


# @admin.route("/user/<uuid>", methods=['GET'])
# @admin_required()
# def get_admin_user(uuid):
#     """
#     Simply checks the connection status and if the application exists.
#
#     :return: JSON-form representing aliveness?
#     """
#     if not Utilities.is_valid_uuid(uuid):
#         return Utilities.return_response(400, "Expected UUID, received something else.")
#
#     local_user = User.query.filter_by(uuid=uuid).first()
#
#     if local_user is None:
#         return Utilities.return_response(404, f"User <{uuid}> not found.")
#
#     return Utilities.generate_public_user_payload(local_user)
