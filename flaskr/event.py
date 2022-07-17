from flask import Blueprint
from flask_jwt_extended import get_jwt_identity

from models.data import Data
from models.event import Event
from models.user import User
from services.utilities import Utilities, user_required

# Configure blueprint
event = Blueprint('event', __name__, url_prefix='/event')


@event.route("/current", methods=['GET'])
@user_required()
def get_event_current():
    """
    Retrieves current event and return it's UUID.

    :return: JSON result response with (current event) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()
    current_event = Event.query.filter_by(active=True).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.response(500, "No active event exists.")

    return Utilities.return_result(200, "Successfully fetched current event", {"uuid": current_event.uuid})


@event.route("/<uuid>", methods=['GET'])
@user_required()
def get_event_by_uuid(uuid):
    """
    Retrieves specific event by UUID and returns its data.

    :return: JSON result response with (event) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    current_event = Event.query.filter_by(uuid=uuid).first()

    # Check if an event exists in the first place
    if current_event is None:
        return Utilities.response(404, f"No event found with UUID: {uuid}.")

    return Utilities.return_result(200, "Successfully fetched current event", current_event)


@event.route("/all", methods=['GET'])
@user_required()
def get_event_all():
    """
    Retrieves all current events and posts their status and UUID.

    :return: JSON result response with (events) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    local_events = Event.query.all()

    if local_events is None or local_events == []:
        return Utilities.response(404, "No events found")

    return Utilities.return_result(200, "Successfully fetched current events", local_events)


@event.route("/last_changed", methods=['GET'])
@user_required()
def get_event_last_changed():
    """
    Retrieves last changed timestamp and hash, indicating changes if different.

    :return: JSON result response with (last_changed) data.
    """
    current_user = User.query.filter_by(uuid=get_jwt_identity()).first()

    if current_user is None:
        return Utilities.response(401, "Unauthorized")

    data = Data.query.first()

    return Utilities.return_result(200, "Successfully fetched events last changed",
                                   {"products_hash": data.events_hash,
                                    "products_last_changed": data.events_last_changed})
