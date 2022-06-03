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
def get_populate_products():
    """
    Populate all products in the database.\n
    This is retrieved from the products.json.

    :return: JSON result of operation.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "ADMIN_POPULATE_PRODUCTS"
    user.last_action_at = datetime.utcnow()

    db_session.commit()
    start_time = datetime.now()

    # Load in file
    from json import load
    result = load(open("./static/products.json"))["products"]

    # Remove old entries
    db_session.query(Product).delete()

    count = 0
    for product in result:
        count += 1
        new_product = Product(id=product["id"],
                              uuid=str(uuid4()),
                              name=product["name"],
                              brand=product["brand"],
                              price=product["price"],

                              category=product["category"],
                              description=product["description"],
                              image=product["image"],
                              image_path=product["image_path"],
                              original_link=product["original_link"],

                              nutri_score=product["nutri_score"].upper(),
                              quantity=product["quantity"],
                              allergens=product["allergens"],
                              ingredients=product["ingredients"],

                              energy=product["energy"],
                              fat=product["fat"],
                              saturated_fat=product["saturated_fat"],
                              unsaturated_fat=product["unsaturated_fat"],
                              carbohydrates=product["carbohydrates"],
                              sugars=product["sugars"],
                              fiber=product["fiber"],
                              proteins=product["proteins"],
                              salt=product["salt"],
                              extra=product["extra"])
        db_session.add(new_product)

    # Rehash and re-stamp
    data = Data.query.first()
    data.generate_hash("products")
    data.generate_timestamp("products")

    db_session.add(data)
    db_session.commit()

    time = round((datetime.now() - start_time).total_seconds() * 1000, 2)
    return Utilities.return_complex_response(200, f"Successfully repopulated {count} products in {time}ms",
                                             {"count": count,
                                              "time": f"{time}ms"
                                              })
