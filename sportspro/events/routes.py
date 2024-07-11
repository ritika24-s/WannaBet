import os
import traceback
from flask import Blueprint, request, jsonify, abort

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
        if not request.get_json():
            abort(400, "Invalid input: No data provided")
            
        data = request.get_json(force=True)
        status_code, message = event_views.create_event(data)

        if status_code == 201:
            return jsonify({'id': message}), 201
        if status_code >= 400:
            return jsonify({"error_message": message}), status_code
        
    except Exception as e:
        logger.error(f"Error creating event: {e}")
        abort(500, 'Failed to create event')

# Endpoint to update an existing event
@events_bp.route('/<int:event_id>', methods=["PATCH", "PUT"])
def update_event(event_id):
    try:
        if not request.get_json():
            abort(400, "Invalid input: No data provided")

        status_code, message = event_views.update_event(int(event_id), request.get_json(force=True))
        
        if status_code == 200:
                return jsonify({"id": int(event_id)}), 200
        if status_code>=400:
            return jsonify({"error_message": message}), status_code
    
    except Exception as e:
        logger.error(f"Error updating event: {e}")
        traceback.print_exc()
        abort(500, 'Failed to update event')

# Endpoint to search for events based on specified criteria
@events_bp.route('/search', methods=["POST"])
def search_particular_event():
    try:
        if not request.get_json():
            return jsonify({"error_message": "Invalid input: No data provided"}), 400

        _, events = event_views.search_events(request.get_json(force=True))
        if events:
            return jsonify({"events": events}), 200
        return jsonify({"error_message": "No data found for the given filters"}), 404
    
    except Exception as e:
        logger.error(f"Error searching for events: {e}")
        traceback.print_exc()
        abort(500, "Internal Server Error")
    
# Endpoint to update status of event
@events_bp.route('/status/<event_name>', methods=["PUT"])
def check_and_update_status_event(event_name):
    try:
        status_code, active_status = event_views.check_and_update_event_inactive_status(event_name=event_name)
        
        if status_code == 200:
            return jsonify({"active_status": active_status}), 200
        if status_code>=400:
            return jsonify({"error_message": f"Status couldnt be updated for {event_name}"}), status_code
        
        abort(status_code, f"Status couldnt be updated for {event_name}")
    except Exception as e:
        abort(500, str(e))