from flask import Blueprint, request, jsonify, abort

from .views import SportsViews
from ..utils.logger import get_logger

# Set up logging
logger = get_logger(__name__)

# Create a sports blueprint
sports_bp = Blueprint('sport', __name__, url_prefix="/sport")
sports_views = SportsViews()

# Endpoint to create a new sport.
@sports_bp.route('/', methods=["POST"])
def create_new_sport():
    """
    Create a new sport.
    Expects a JSON payload with sport details.
    """
    try:
        if not request.get_json():
            abort(400, "Invalid input: No data provided")
        status_code, message = sports_views.create_sport(data=request.get_json())
        if status_code == 201:
            return jsonify({"id": int(message)}), 201
        else:
            abort(status_code, str(message))
    
    except Exception as e:
        logger.error(f"Error creating new sport: {e}")
        abort(500, "Internal Server Error")

# Endpoint to update or delete an existing sport
@sports_bp.route('/<int:sport_id>', methods=["PATCH", "DELETE"])
def update_sport(sport_id):
    """
    Update or delete an existing sport.
    PATCH: Expects a JSON payload with updated sport details.
    DELETE: Deletes the specified sport.
    """
    try:
        if not request.get_json():
            abort(400, "Invalid input: No data provided")

        if request.method == "DELETE":
            message, status_code = sports_views.delete_sport(sport_id=int(sport_id), data=request.get_json())

            if status_code == 200:
                return jsonify({'id':sport_id}), 200
            abort(status_code, str(message))
        
        else:
            status_code, message = sports_views.update_sport(sport_id, request.get_json())
            if status_code == 200:
                return jsonify({"id": int(sport_id)}), 200
            else:
                abort(status_code, str(message))

    except ValueError as e:
        logger.error(f"ValueError: {e}")
        abort(400, str(e))
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        abort(404, str(e))
    except Exception as e:
        logger.error(f"Error updating/deleting sport: {e}")
        abort(500, "Internal Server Error")

# Endpoint to search for sports based on specified criteria
@sports_bp.route('/search', methods=["POST"])
def search_particular_sport():
    """
    Search for sports based on specified criteria.
    Expects a JSON payload with search filters.
    """
    try:
        if not request.get_json():
            abort(400, "Invalid input: No data provided")
            
        sports = sports_views.search_sport(request.get_json())
        if sports:
            return jsonify({"sports": sports}), 200
        abort(404, "No data found for the given filters")
    
    except Exception as e:
        logger.error(f"Error searching for sports: {e}")
        abort(500, "Internal Server Error")

# Endpoint to get all sports
@sports_bp.route('/', methods=["GET"])
def get_all_sports():
    try:
        sports = sports_views.get_sports_list()
        return jsonify({"sports": sports}), 200
    except Exception as e:
        abort(500, str(e))

# Endpoint to update status of sports
@sports_bp.route('/status/<int:sport_id>', methods=["PUT"])
def check_and_update_status_sport(sport_id):
    try:
        active_status, status_code = sports_views.check_and_update_sport_inactive_status(sport_id=sport_id)
        if status_code == 200:
            return jsonify({"active_status": active_status}), 200
        abort(f"Status couldnt be updated for {sport_id}", status_code)
    except Exception as e:
        abort(500, str(e))