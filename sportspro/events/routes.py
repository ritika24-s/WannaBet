import os
from flask import Blueprint, request, jsonify, abort

# from sportspro import app

from .views import EventsViews
from ..utils.logger import get_logger
logger = get_logger(__name__)

# Create a events blueprint
events_bp = Blueprint('event', __name__, url_prefix="/event")
event_views = EventsViews()

# Endpoint to create a new event
@events_bp.route('/', methods=["POST"])
def create_event():
    try:
        event_id = event_views.create_event(request.get_json())
        return jsonify({'id': event_id}), 201
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        abort(500, 'Failed to create event')

# Endpoint to update an existing event
@events_bp.route('/<int:event_id>', methods=["PATCH"])
def update_event(event_id):
    try:
        data = request.get_json()
        updated_event_id = event_views.update_event(event_id, data)
        return jsonify({'id': updated_event_id})
    except Exception as e:
        logger.error(f"Error updating event: {e}")
        abort(500, 'Failed to update event')

# Endpoint to search for events based on specified criteria
@events_bp.route('/search', methods=["POST"])
def search_particular_sport():
    try:
        events = event_views.search_events(request.get_json())
        return jsonify({'events': events}), 200
    except Exception as e:
        logger.error(f"Error searching events: {e}")
        return jsonify({'error': 'Failed to search events'}), 500