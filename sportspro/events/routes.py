import os
from flask import Blueprint, request, jsonify

# from sportspro import app

from .views import EventsViews
from ..utils.logger import setup_logger
from ..config import config_by_name

# config = config_by_name[os.getenv('FLASK_ENV', 'development')]
config = config_by_name["development"]
logger = setup_logger(config.LOG_LEVEL)

# Create a events blueprint
events_bp = Blueprint('events', __name__, url_prefix="/events")
event_views = EventsViews()

# Endpoint to create a new event
@events_bp.route('/', methods=["POST"])
def create_event():
    try:
        data = request.get_json()
        event_id = event_views.create_event(data)
        return jsonify({'id': event_id}), 201
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        return jsonify({'error': 'Failed to create event'}), 500

# Endpoint to update an existing event
@events_bp.route('/<event_id>', methods=["UPDATE"])
def update_event(event_id):
    try:
        data = request.get_json()
        updated_event_id = event_views.update_event(event_id, data)
        return jsonify({'id': updated_event_id})
    except Exception as e:
        logger.error(f"Error updating event: {e}")
        return jsonify({'error': 'Failed to update event'}), 500

# Endpoint to search for events based on specified criteria
@events_bp.route('/search', methods=["POST"])
def search_particular_sport():
    try:
        filters = request.get_json()
        events = event_views.search_events(filters)
        return jsonify({'events': events})
    except Exception as e:
        logger.error(f"Error searching events: {e}")
        return jsonify({'error': 'Failed to search events'}), 500