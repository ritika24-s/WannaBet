from flask import Blueprint, request, jsonify

from sportspro import app
from .views import SportsViews

# Create a sports blueprint
sports_bp = Blueprint('sports', __name__, url_prefix="/sports")
sports_views = SportsViews()

# Endpoint to create a new sport.
@sports_bp.route('/', methods=["POST"])
def create_new_sport():
    data = request.get_json()
    if data:
        sport_id, status = sports_views.create_sport(data)
    if status==201:
        return jsonify({'id': sport_id}), status
    return {"message":"error", "status":400}

# Endpoint to update an existing sport
@sports_bp.route('/<sport_id>', methods=["UPDATE"])
def update_sport(sport_id):
    results = sports_views.update_sport(sport_id, request.get_json())
    

# Endpoint to search for sports based on specified criteria
@sports_bp.route('/search', methods=["POST"])
def search_particular_sport():
    pass