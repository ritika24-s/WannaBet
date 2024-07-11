import pytest
import json

from ..utils.logger import get_logger

logger = get_logger(__name__)

events = [
    {
        "id": 1,
        "name": "Arsenal vs Leeds",
        "slug": "arsenal-vs-leeds",
        "active": True,
        "type": "preplay",
        "sport": "Football",
        "status": "PENDING",
        "scheduled_start": "2024-07-01T15:00:00Z",
        "actual_start": None,
        "logos": "link_1|link_2"
    },
    {
        "id": 2,
        "name": "Lakers vs Heat",
        "slug": "lakers-vs-heat",
        "active": True,
        "type": "inplay",
        "sport": "Basketball",
        "status": "STARTED",
        "scheduled_start": "2024-07-02T18:00:00Z",
        "actual_start": "2024-07-02T18:05:00Z",
        "logos": "link_3|link_4"
    },
    {
        "id": 3,
        "name": "Federer vs Nadal",
        "slug": "federer-vs-nadal",
        "active": False,
        "type": "preplay",
        "sport": "Tennis",
        "status": "CANCELLED",
        "scheduled_start": "2024-07-03T12:00:00Z",
        "actual_start": None,
        "logos": "link_5|link_6"
    }
]


def test_create_event(client):
    data = {
        "name": "Chelsea vs Manchester United",
        "slug": "chelsea-vs-manchester-united",
        "active": True,
        "type": "preplay",
        "sport": "Football",
        "status": "PENDING",
        "scheduled_start": "2024-07-04T15:00:00Z",
     }
    logger.debug("Starting test_create_event")

    response = client.post("/event/", json=data)
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_update_event(client):
    """
    Test updating an existing event.
    """
    logger.debug("Starting test_update_event")

    updated_data = {
        "logos": "|"
        }
    
    response = client.put("/event/2", json=updated_data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 200
    assert "id" in response.get_json()

def test_update_event_with_wrong_status(client):
    """
    Test updating an existing event with value outside ENUM
    """
    logger.debug("Starting test_update_event")

    updated_data = {
        "status": "completed"
        }
    
    response = client.patch("/event/1", json=updated_data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 400
    assert "error_message" in response.get_json()
    assert response.get_json()["error_message"] == "Status value is not acceptable"

def test_search_events(client):
    """
    Test searching for event based on filters.
    """
    logger.debug("Starting test_search_event")
    # Create a event for search
    event_data = {
        "name": "Real Madrid vs Manchester United",
        "slug": "real-madrid-vs-manchester-united",
        "active": True,
        "type": "inplay",
        "sport": "Football",
        "status": "PENDING",
        "scheduled_start": "2024-07-04T15:00:00Z",
    }
    client.post('/event/', json=event_data, content_type='application/json')

    search_data = {
        "name": "Real Madrid vs Manchester United"
    }
    response = client.post("/event/search", json=search_data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 200
    data = response.get_json()
    assert "events" in data
    assert len(data["events"]) > 0

# def test_delete_event(client):
#     response = client.delete("/event/1")
#     assert response.status_code == 200

def test_search_event_by_name_regex(client):
    response = client.post("/event/search", json={"name_regex": "Match.*"})
    assert response.status_code == 200
    assert "events" in response.get_json()

def test_search_event_by_timeframe(client):
    response = client.post("/event/search", json={"scheduled_start_from": "2024-07-01 00:00:00", "scheduled_start_to": "2024-07-31 23:59:59"})
    assert response.status_code == 200
    assert "events" in response.get_json()

