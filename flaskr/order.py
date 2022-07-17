from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.data import Data
from models.event import Event
from models.user import User
from models.order import Order
from models.product import Product
from services.database import db_session
from services.utilities import Utilities

# Configure blueprint
order = Blueprint('order', __name__, url_prefix='/order')


@order.route("/current", methods=['GET'])
@jwt_required()
def get_order_current():
    """
    Gets the current order for the current event for the user.

    :return: JSON result response with (current order) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    current_event = Event.query.filter_by(active=True).first()

    if current_event is None:
        return Utilities.response(500, "No current event exists.")

    # Check if an order exists.
    current_order = Order.query.filter_by(user=current_user.uuid, event=current_event.uuid).first()

    if current_order is None:
        return Utilities.response(404, "No order for current event exists, use /order/add instead.")

    return Utilities.return_result(200, "Successfully retrieved current order", {"uuid": current_order.uuid,
                                                                                 "products": current_order.products,
                                                                                 "notes": current_order.notes})


@order.route("/<uuid>", methods=['GET'])
@jwt_required()
def get_order_by_uuid(uuid):
    """
    Gets an order by uuid for the user.

    :return: JSON result response with (order by uuid) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    # Check if an order exists.
    current_order = Order.query.filter_by(user=current_user.uuid, uuid=uuid).first()

    if current_order is None:
        return Utilities.response(404, f"No order found with UUID: {uuid}.")

    return Utilities.return_result(200, "Successfully retrieved current order", current_order)


@order.route("/event/<uuid>", methods=['GET'])
@jwt_required()
def get_order_by_event(uuid):
    """
    Gets an order sorted by event for the user.

    :return: JSON result response with (order by event uuid) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    # Check if an order exists.
    current_order = Order.query.filter_by(user=current_user.uuid, event=uuid).first()

    if current_order is None:
        return Utilities.response(404, f"No order found with linked to event: {uuid}.")

    return Utilities.return_result(200, f"Successfully retrieved order for event {uuid}", current_order)


@order.route("/all", methods=['GET'])
@jwt_required()
def get_order_all_for_user():
    """
    Gets all orders sorted by uuid for the user.

    :return: JSON result response with a (list of events) data.
    """
    # TODO: Look at the check for emptiness
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    # Check if any orders exist
    current_order_list = Order.query.filter_by(user=current_user.uuid).all()

    if current_order_list is None or current_order_list == []:
        return Utilities.response(404, "No orders found for any events.")

    return Utilities.return_result(200, f"Successfully retrieved {len(current_order_list)} orders", current_order_list)


@order.route("/add", methods=['POST'])
@jwt_required()
def post_order_add():
    """
    Adds an order to the current event for the user.

    :return: JSON detailed status response with (created event uuid) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    current_event = Event.query.filter_by(active=True).first()

    if current_event is None:
        return Utilities.response(500, "No current event exists.")

    # Check if an order already exists.
    current_order = Order.query.filter_by(user=current_user.uuid, event=current_event.uuid).first()

    if current_order is not None:
        return Utilities.detailed_response(409, "Order for current event already exists, use /order/edit instead.",
                                           {"uuid": current_order.uuid})

    try:
        # TODO: Turn this validation into a utility
        user = current_user.uuid
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
        return Utilities.detailed_response(400, "Bad request, see details.", {"error": e.__str__()})

    new_order = Order(
        user=user,
        products=products,
        total_price=total_price,
        notes=notes,
        event=event.uuid,
    )

    db_session.add(new_order)
    db_session.commit()

    # Rehash and re-stamp
    data = Data.query.first()
    data.perform_changes("orders")

    current_user.perform_tracking(address=request.remote_addr)

    return Utilities.detailed_response(201, "Successfully created new order", {"order": {"products": products,
                                                                                               "event": event.uuid,
                                                                                               "notes": notes,
                                                                                               "price": total_price}})


@order.route("/delete", methods=['DELETE'])
@jwt_required()
def delete_order_current():
    """
    Deletes an existing order for the current event for the user.

    :return: JSON detailed status response with (deletec event uuid) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    current_event = Event.query.filter_by(active=True).first()

    if current_event is None:
        return Utilities.response(500, "No current event exists.")

    # Check if an order exists.
    current_order = Order.query.filter_by(user=current_user.uuid, event=current_event.uuid).first()
    if current_order is None:
        return Utilities.response(404, "No order for current event exists, use /order/add instead.")

    uuid = current_order.uuid
    old = current_order.__repr__()

    db_session.delete(current_order)
    db_session.commit()

    # Rehash and re-stamp
    data = Data.query.first()
    data.perform_changes("orders")

    current_user.perform_tracking(address=request.remote_addr)

    return Utilities.detailed_response(200, f"Successfully deleted {old}", {"order": {"uuid": uuid}})


@order.route("/edit", methods=['PUT'])
@jwt_required()
def put_order_edit():
    """
    Edits an existing order for the current event for the user.

    :return: JSON detailed status response with (new order) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    current_event = Event.query.filter_by(active=True).first()

    if current_event is None:
        return Utilities.response(500, "No current event exists.")

    # Check if an order exists.
    current_order = Order.query.filter_by(user=current_user.uuid, event=current_event.uuid).first()

    if current_order is None:
        return Utilities.response(404, "No order for current event exists, use /order/add instead.")

    try:
        # TODO: Turn this validation into a utility
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
        return Utilities.detailed_response(400, "Bad request, see details.", {"error": e.__str__()})

    current_order.products = products
    current_order.total_price = total_price
    current_order.notes = notes

    db_session.commit()

    # Rehash and re-stamp
    data = Data.query.first()
    data.perform_changes("orders")

    current_user.perform_tracking(address=request.remote_addr)

    return Utilities.detailed_response(200, f"Successfully edited {current_order}",
                                       {"order": {"products": current_order.products,
                                                        "event": event.uuid,
                                                        "notes": current_order.notes,
                                                        "price": current_order.total_price}})


@order.route("/last_changed", methods=['GET'])
@jwt_required()
def get_order_last_changed():
    """
    Retrieves last changed timestamp and hash, indicating changes if different.

    :return: JSON result response with (last changed) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")
    current_user.perform_tracking(address=request.remote_addr)

    data = Data.query.first()

    return Utilities.return_result(200, "Successfully fetched orders last changed",
                                   {"products_hash": data.orders_hash,
                                    "products_last_changed": data.orders_last_changed})
