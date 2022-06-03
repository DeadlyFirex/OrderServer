from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.data import Data
from models.event import Event
from models.user import User
from services.config import Config
from services.database import db_session
from services.utilities import Utilities

from datetime import datetime

config = Config().get_config()
event = Blueprint('event', __name__, url_prefix='/event')


@event.route("/current", methods=['GET'])
@jwt_required()
def get_event():
    """
    Retrieves current event and return it's UUID.

    :return: JSON-form representing aliveness?
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()
    current_event = Event.query.filter_by(active=True).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_CURRENT_EVENT"
    user.last_action_at = datetime.utcnow()

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.return_response(500, "No current event exists.")

    db_session.commit()

    return Utilities.return_result(200, "Successfully fetched current event", {"uuid": current_event.uuid})


@event.route("/<uuid>", methods=['GET'])
@jwt_required()
def get_event_by_uuid(uuid):
    """
    Retrieves specific event by UUID and returns its data.

    :return: JSON-form representing aliveness?
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()
    current_event = Event.query.filter_by(uuid=uuid).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_CURRENT_EVENT"
    user.last_action_at = datetime.utcnow()

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.return_response(404, f"No event found with UUID: {uuid}.")

    db_session.commit()

    return Utilities.return_result(200, "Successfully fetched current event", current_event)


@event.route("/all", methods=['GET'])
@jwt_required()
def get_all_events():
    """
    Retrieves all current events and posts their status and UUID.

    :return: JSON with result template.
    """
    user = User.query.filter_by(uuid=get_jwt_identity()).first()
    current_event = Event.query.filter_by(active=True).first()

    if user is None:
        return Utilities.return_response(401, "Unauthorized")

    user.active = True
    user.last_login_at = datetime.utcnow()
    user.last_login_ip = request.remote_addr
    user.last_action = "GET_CURRENT_EVENT"
    user.last_action_at = datetime.utcnow()

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.return_response(500, "No current event exists.")

    local_events = Event.query.all()

    if local_events is None or local_events == []:
        return Utilities.return_response(404, "No events found")

    db_session.commit()

    return Utilities.return_result(200, "Successfully fetched current events", local_events)


@event.route("/last_changed", methods=['GET'])
@jwt_required()
def get_events_last_changed():
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

    return Utilities.return_result(200, "Successfully fetched events last changed",
                                   {"products_hash": data.events_hash,
                                    "products_last_changed": data.events_last_changed})
