import pytest
import json
from ..utils.logger import get_logger
from sportspro.db import DB

logger = get_logger(__name__)

@pytest.fixture(scope="module")
def db():
    # Initialize the database and create some initial test data
    db = DB()

    # # Insert initial data for testing
    # db.execute_query(
    #     query="INSERT INTO sports (name, slug, active) VALUES (%s, %s, %s)",
    #     values=("Chess", "chess", True)
    # )
    # delete data before tests
    db.execute_query("DELETE from sports;")
    db.execute_query("ALTER TABLE sports AUTO_INCREMENT = 1;")
       
    yield db

    # # delete data after tests
    # db.execute_query("DELETE FROM sports;")
    # db.execute_query("ALTER TABLE sports AUTO_INCREMENT = 1;")

    


def test_create_sport(client, db):
    """
    Test creating a new sport.
    """
    logger.debug("Starting test_create_sport")
    sport_data = {
        "name": "Soccer",
        "slug": "soccer",
        "active": True
    }
    response = client.post('/sport/', json=sport_data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 201
    assert 'id' in response.json

def test_create_duplicate_sport(client):
    """
    Test creating a duplicate sport (should fail).
    """
    logger.debug("Starting test_create_duplicate_sport")
    sport_data = {
        "name": "Soccer",
        "slug": "soccer",
        "active": True
    }
    response = client.post('/sport/', json=sport_data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 409

def test_update_sport(client):
    """
    Test updating an existing sport.
    """
    logger.debug("Starting test_update_sport")
    updated_data = {
        "active": False
    }
    response = client.patch('/sport/1', json=updated_data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 200
    assert response.json['id'] == 1

def test_get_all_sports(client):
    """
    Test retrieving all sports.
    """
    logger.debug("Starting test_get_all_sports")
    response = client.get('/sport/', content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 200
    assert isinstance(response.json['sports'], list)

def test_search_sport(client):
    """
    Test searching for sports based on filters.
    """
    logger.debug("Starting test_search_sport")
    # Create a sport for search
    sport_data = {
        "name": "Basketball",
        "slug": "basketball",
        "active": True
    }
    client.post('/sport/', json=sport_data, content_type='application/json')

    search_data = {
        "name": "Basketball",
        "active": True
    }
    response = client.post('/sport/search', json=search_data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 200
    assert len(response.json['sports']) > 0
    assert response.json['sports'][0]['name'] == "Basketball"

def test_update_sport_status(client):
    response = client.post("/sport/", json={"name": "Rugby", "slug": "rugby", "active": True})
    sport_id = response.json["id"]
    response = client.put("/sport/status/Rugby")
    assert response.status_code == 200
    assert response.json["active_status"] is False
