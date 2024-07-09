import pytest
from sportspro.db import DB
import json

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

@pytest.fixture
def init_database():
    # Initialize the database and create some initial test data
    db = DB()
    db.create_all()

    # Insert initial data for testing
    db.execute_query(
        "INSERT INTO events (name, slug, active, type, sport, status, scheduled_start, actual_start, logos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        ("Test Event 1", "test-event-1", True, "type1", "sport1", "scheduled", "2023-07-01 10:00:00", None, "logo1.png")
    )
    
    yield db

    # Drop all tables after tests
    db.drop_all()

def test_create_new_event():
    event = {
    "name": "Chelsea vs Manchester United",
    "slug": "chelsea-vs-manchester-united",
    "active": True,
    "type": "preplay",
    "sport": "Football",
    "status": "PENDING",
    "scheduled_start": "2024-07-04T15:00:00Z",
    "logos": "link_7|link_8"
}
    
def test_update_event():
    event ={
    "name": "Chelsea vs Manchester United",
    "slug": "chelsea-vs-manchester-united",
    "active": True,
    "type": "preplay",
    "sport": "Football",
    "status": "STARTED",
    "scheduled_start": "2024-07-04T15:00:00Z",
    "actual_start": "2024-07-04T15:05:00Z",
    "logos": "link_7|link_8"
}

def test_search_event():
    search = {
    "sport": "Football",
    "status": "PENDING"
}
def test_create_event(client, init_database):
    response = client.post("/events/", json={
        "name": "Event 2",
        "slug": "event-2",
        "active": True,
        "type": "type2",
        "sport": "sport2",
        "status": "scheduled",
        "scheduled_start": "2023-07-01 10:00:00",
        "actual_start": None,
        "logos": "logo2.png"
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_update_event(client, init_database):
    response = client.patch("/events/1", json={
        "name": "Updated Event 1",
        "slug": "updated-event-1",
        "active": False,
        "type": "type1",
        "sport": "sport1",
        "status": "completed",
        "scheduled_start": "2023-07-01 10:00:00",
        "actual_start": "2023-07-01 12:00:00",
        "logos": "updated_logo1.png"
    })
    assert response.status_code == 200
    assert "id" in response.get_json()

def test_search_events(client, init_database):
    response = client.post("/events/search", json={"name": "Test Event"})
    assert response.status_code == 200
    data = response.get_json()
    assert "events" in data
    assert len(data["events"]) > 0

def test_delete_event(client, init_database):
    response = client.delete("/events/1")
    # assert response.status_code ==

