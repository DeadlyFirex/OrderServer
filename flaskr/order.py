from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.database import db_session
from models.event import Event
from models.user import User
from models.order import Order
from models.product import Product
from services import config
from services.utilities import Utilities, admin_required

from datetime import datetime
from uuid import uuid4

config = config.Config().get_config()
order = Blueprint('order', __name__, url_prefix='/order')


@order.route("/add", methods=['POST'])
@jwt_required()
def post_order():
    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_unauthorized()

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_ALL_PRODUCTS"
    user.last_action_at = datetime.utcnow()

    try:
        user = user.uuid
        notes = request.json.get("notes", None)
        total_price = 0.0
        event = Event.query.filter_by(active=True).first()
        products = request.json.get("products", None)

        if not isinstance(products, list):
            raise AttributeError(f"Expected list, instead got {type(products)}")
        for product in products:
            if not isinstance(product, str):
                raise AttributeError(f"Field <{product}> in products field is not str")
            product_query = Product.query.filter_by(uuid=product).first()
            if product_query is None:
                raise AttributeError(f"Product <{product}> was not found")
            total_price += product_query.price

        if total_price > event.max_order_price:
            raise AttributeError(f"Price exceeded maximum: <{event.max_order_price}>")

    except AttributeError as e:
        return {"status": 400, "message": e.__str__()}

    new_order = Order(
        user=user,
        products=products,
        total_price=total_price,
        notes=notes,
        event=event.uuid,
    )

    db_session.add(new_order)
    db_session.commit()

    return Utilities.return_success()