import pytest
from flask import Response

from sportspro.sports.models import SportsModels
from sportspro.sports.views import SportsViews
from sportspro import create_app
from ..config import *

sports = [
    {
        "name": "Football",
        "slug": "football",
        "active": True
    },
    {
        "name": "Basketball",
        "slug": "basketball",
        "active": True
    },
    {
        "name": "Tennis",
        "slug": "tennis",
        "active": False
    }
]

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(DevelopmentConfig)
    
    return app

@pytest.fixture
def client(app):
    app.testing = True
    return app.test_client()

@pytest.fixture
def sports_views():
    return SportsViews()

def test_delete_sport(client):
    response = client.delete("/sport/1", json={"name":"Rugby"})
    assert response.status_code == 200

def test_create_new_sport(client, sports_views):
    _,_ = sports_views.delete_sport(sport_id=1, data={"name":"Rugby"})

    body = {
    "name": "Rugby",
    "slug": "rugby",
    "active": True
    }
    
    status_code, message  = sports_views.create_sport(body)
    assert status_code == 201
    assert isinstance(message, int)

# def test_create_sport_missing_name(client):
#     data = {
#         "slug": "football",
#         "active": True
#     }
#     response = client.post("/sport/", json=data)
#     assert response.status_code == 400
#     assert "error_message" in response.get_json()

# def test_update_sport():
#     sport = {
#     "name": "Rugby",
#     "slug": "rugby",
#     "active": False
#     }
    
# def test_get_sport():
#     search_data = {
#     "name": "Football",
#     "active": True
# }
    


# def test_update_sport(client, sport_service):
#     # First, create a sport
#     create_data = {
#         "name": "Basketball",
#         "slug": "basketball",
#         "active": True
#     }
#     create_response = client.post("/sport/", json=create_data)
#     sport_id = create_response.get_json()["id"]

#     # Now, update the sport
#     update_data = {
#         "name": "Updated Basketball"
#     }
#     update_response = client.patch(f"/sport/{sport_id}", json=update_data)
#     assert update_response.status_code == 200
#     assert update_response.get_json()["id"] == sport_id

# def test_update_nonexistent_sport(client, sport_service):
#     update_data = {
#         "name": "Nonexistent Sport"
#     }
#     response = client.patch("/sport/9999", json=update_data)
#     assert response.status_code == 404
#     assert "error_message" in response.get_json()

# def test_search_sports(client, sport_service):
#     # First, create a sport
#     create_data = {
#         "name": "Tennis",
#         "slug": "tennis",
#         "active": True
#     }
#     client.post("/sport/", json=create_data)

#     # Now, search for the sport
#     search_data = {
#         "name": "Tennis"
#     }
#     search_response = client.post("/sport/search", json=search_data)
#     assert search_response.status_code == 200
#     sports = search_response.get_json()["sports"]
#     assert len(sports) > 0
#     assert sports[0]["name"] == "Tennis"