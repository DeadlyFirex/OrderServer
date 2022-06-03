from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.data import Data
from models.event import Event
from models.user import User
from models.order import Order
from models.product import Product
from services.database import db_session
from services.utilities import Utilities

from datetime import datetime

# Configure blueprint
order = Blueprint('order', __name__, url_prefix='/order')


@order.route("/current", methods=['GET'])
@jwt_required()
def get_order():
    """
    Gets the current order for the current event for the user.

    :return: JSON response.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()
    current_event = Event.query.filter_by(active=True).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "POST_CURRENT_ORDER"
    user.last_action_at = datetime.utcnow()

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.return_response(500, "No current event exists.")

    # Check if an order exists.
    check = Order.query.filter_by(user=user.uuid, event=current_event.uuid).first()
    if check is None:
        return Utilities.return_response(404, "No order for current event exists, use /order/add instead.")


    db_session.commit()

    return Utilities.return_result(200, "Successfully retrieved current order", {"uuid": check.uuid,
                                                                                 "products": check.products,
                                                                                 "notes": check.notes})


@order.route("/<uuid>", methods=['GET'])
@jwt_required()
def get_order_by_uuid(uuid):
    """
    Gets an order sorted by UUID for the user.

    :return: JSON response.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_SPECIFIC_ORDER"
    user.last_action_at = datetime.utcnow()

    # Check if an order exists.
    current_order = Order.query.filter_by(user=user.uuid, uuid=uuid).first()
    if current_order is None:
        return Utilities.return_response(404, f"No order found with UUID: {uuid}.")

    db_session.commit()

    return Utilities.return_result(200, "Successfully retrieved current order", current_order)


@order.route("/event/<uuid>", methods=['GET'])
@jwt_required()
def get_order_by_event(uuid):
    """
    Gets an order sorted by event for the user.

    :return: JSON response.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_SPECIFIC_ORDER"
    user.last_action_at = datetime.utcnow()

    # Check if an order exists.
    current_order = Order.query.filter_by(user=user.uuid, event=uuid).first()
    if current_order is None:
        return Utilities.return_response(404, f"No order found with linked to event: {uuid}.")

    db_session.commit()

    return Utilities.return_result(200, f"Successfully retrieved order for event {uuid}", current_order)


@order.route("/all", methods=['GET'])
@jwt_required()
def get_all_orders():
    """
    Gets all orders sorted by UUID for the user.

    :return: JSON response.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_SPECIFIC_ORDER"
    user.last_action_at = datetime.utcnow()

    local_events = Order.query.filter_by(user=user.uuid).all()

    if local_events is None or local_events == []:
        return Utilities.return_response(404, "No events found.")

    db_session.commit()

    return Utilities.return_result(200, f"Successfully retrieved {len(local_events)} orders", local_events)


@order.route("/add", methods=['POST'])
@jwt_required()
def post_order():
    """
    Adds an order to the current event for the user.

    :return: JSON response.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()
    current_event = Event.query.filter_by(active=True).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "POST_CURRENT_ORDER"
    user.last_action_at = datetime.utcnow()

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.return_response(500, "No current event exists.")

    # Check if an order already exists.
    check = Order.query.filter_by(user=user.uuid, event=current_event.uuid).first()
    if check is not None:
        return Utilities.return_complex_response(409, "Order for current event already exists, use /order/edit instead.",
                                                 {"uuid": check.uuid})

    try:
        user = user.uuid
        total_price = 0.0
        event = current_event
        notes = request.json.get("notes", None)
        products = request.json.get("products", None)

        if not isinstance(products, list):
            raise AttributeError(f"Expected list, instead got {type(products)}")
        if not isinstance(notes, str) and notes is not None:
            raise AttributeError(f"Expected string, instead got {type(notes)}")
        for product in products:
            if not isinstance(product, str):
                raise AttributeError(f"Field <{product}> in product list is not str")
            product_query = Product.query.filter_by(uuid=product).first()
            if product_query is None:
                raise AttributeError(f"Product <{product}> was not found")
            total_price += product_query.price

        if total_price > event.max_order_price:
            raise AttributeError(f"Price exceeded maximum: <{event.max_order_price}>")

    except AttributeError as e:
        return Utilities.return_complex_response(400, "Bad request, see details.", {"error": e.__str__()})

    new_order = Order(
        user=user,
        products=products,
        total_price=total_price,
        notes=notes,
        event=event.uuid,
    )

    db_session.add(new_order)

    # Rehash and re-stamp
    data = Data.query.first()
    data.generate_hash("orders")
    data.generate_timestamp("orders")

    db_session.commit()

    return Utilities.return_complex_response(201, "Successfully created new order", {"order": {"products": products,
                                                                                               "event": event.uuid,
                                                                                               "notes": notes,
                                                                                               "price": total_price}})


@order.route("/delete", methods=['DELETE'])
@jwt_required()
def delete_order():
    """
    Deletes an existing order for the current event for the user.

    :return: JSON response.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()
    current_event = Event.query.filter_by(active=True).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "DELETE_CURRENT_ORDER"
    user.last_action_at = datetime.utcnow()

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.return_response(500, "No current event exists.")

    # Check if an order exists.
    check = Order.query.filter_by(user=user.uuid, event=current_event.uuid).first()
    if check is None:
        return Utilities.return_response(404, "No order for current event exists, use /order/add instead.")

    uuid = check.uuid
    old = check.__repr__()

    db_session.delete(check)

    # Rehash and re-stamp
    data = Data.query.first()
    data.generate_hash("orders")
    data.generate_timestamp("orders")

    db_session.commit()

    return Utilities.return_complex_response(200, f"Successfully deleted {old}", {"order": {"uuid": uuid}})


@order.route("/edit", methods=['PUT'])
@jwt_required()
def put_order():
    """
    Edits an existing order for the current event for the user.

    :return: JSON response.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()
    current_event = Event.query.filter_by(active=True).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "POST_CURRENT_ORDER"
    user.last_action_at = datetime.utcnow()

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.return_response(500, "No current event exists.")

    # Check if an order exists.
    current_order = Order.query.filter_by(user=user.uuid, event=current_event.uuid).first()
    if current_order is None:
        return Utilities.return_response(404, "No order for current event exists, use /order/add instead.")

    try:
        total_price = 0.0
        event = current_event
        notes = request.json.get("notes", None)
        products = request.json.get("products", None)

        if not isinstance(products, list):
            raise AttributeError(f"Expected list, instead got {type(products)}")
        if not isinstance(notes, str) and notes is not None:
            raise AttributeError(f"Expected string, instead got {type(notes)}")
        for product in products:
            if not isinstance(product, str):
                raise AttributeError(f"Field <{product}> in product list is not str")
            product_query = Product.query.filter_by(uuid=product).first()
            if product_query is None:
                raise AttributeError(f"Product <{product}> was not found")
            total_price += product_query.price

        if total_price > event.max_order_price:
            raise AttributeError(f"Price exceeded maximum: <{event.max_order_price}>")

    except AttributeError as e:
        return Utilities.return_complex_response(400, "Bad request, see details.", {"error": e.__str__()})

    current_order.products = products
    current_order.total_price = total_price
    current_order.notes = notes

    # Rehash and re-stamp
    data = Data.query.first()
    data.generate_hash("orders")
    data.generate_timestamp("orders")

    db_session.commit()

    return Utilities.return_complex_response(200, f"Successfully edited {current_order}",
                                             {"order": {"products": current_order.products,
                                                        "event": event.uuid,
                                                        "notes": current_order.notes,
                                                        "price": current_order.total_price}})


@order.route("/last_changed", methods=['GET'])
@jwt_required()
def get_orders_last_changed():
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
    user.last_action = "GET_ORDERS_LAST_CHANGED"
    user.last_action_at = datetime.utcnow()

    db_session.commit()

    data = Data.query.first()

    return Utilities.return_result(200, "Successfully fetched orders last changed",
                                   {"products_hash": data.orders_hash,
                                    "products_last_changed": data.orders_last_changed})
