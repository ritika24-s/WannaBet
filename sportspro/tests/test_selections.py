import pytest
from sportspro.db import DB
from ..utils.logger import get_logger

logger = get_logger(__name__)

selections = [
    {
        "id": 1,
        "name": "Arsenal Win",
        "event": "Arsenal vs Leeds",
        "price": 2.50,
        "active": True,
        "outcome": "UNSETTLED"
    },
    {
        "id": 2,
        "name": "Leeds Win",
        "event": "Arsenal vs Leeds",
        "price": 3.00,
        "active": True,
        "outcome": "UNSETTLED"
    },
    {
        "id": 3,
        "name": "Draw",
        "event": "Arsenal vs Leeds",
        "price": 3.20,
        "active": True,
        "outcome": "UNSETTLED"
    },
    {
        "id": 4,
        "name": "Lakers Win",
        "event": "Lakers vs Heat",
        "price": 1.80,
        "active": True,
        "outcome": "UNSETTLED"
    },
    {
        "id": 5,
        "name": "Heat Win",
        "event": "Lakers vs Heat",
        "price": 2.20,
        "active": True,
        "outcome": "UNSETTLED"
    },
    {
        "id": 6,
        "name": "Federer Win",
        "event": "Federer vs Nadal",
        "price": 1.90,
        "active": False,
        "outcome": "VOID"
    },
    {
        "id": 7,
        "name": "Nadal Win",
        "event": "Federer vs Nadal",
        "price": 2.10,
        "active": False,
        "outcome": "VOID"
    }
]
@pytest.fixture(scope="module")
def db():
    # Initialize the database and create some initial test data
    db = DB()

    #  delete data before tests
    db.execute_query("DELETE from selections;")
    db.execute_query("ALTER TABLE selections AUTO_INCREMENT = 1;")

    # Insert initial data for testing
    db.execute_query(
        "INSERT INTO selections (name, event, active, price, outcome) VALUES (%s, %s, %s, %s, %s)",
        ("Draw", "Arsenal vs Leeds", False, 100, "UNSETTLED")
    )
    
    yield db

    # delete data after tests
    # db.execute_query("DELETE from selections;")

# @pytest.fixture
# def test_create_new_selection():
#     selection = {
#     "name": "Chelsea Win",
#     "event": "Chelsea vs Manchester United",
#     "price": 2.30,
#     "active": True,
#     "outcome": "UNSETTLED"
# }

# def test_update_selection():
#     selection = {
#     "name": "Chelsea Win",
#     "event": "Chelsea vs Manchester United",
#     "price": 2.30,
#     "active": False,
#     "outcome": "LOSE"
# }

# def test_search_selection():
#     search = {
#     "event": "Arsenal vs Leeds",
#     "active": True
# }

def test_create_selection(client, db):
    data = {
        "name": "Selection1",
        "active": True,
        "event": "Arsenal vs Leeds",
        "outcome": "UNSETTLED",
        "price": 2.30,
    }
    response = client.post("/selection/", json=data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_update_selection_and_event_status(client):
    # Create an active selection
    data = {
    "name": "Chelsea Win",
    "event": "Chelsea vs Manchester United",
    "price": 2.30,
    "active": True,
    "outcome": "UNSETTLED"
    }
    response = client.post("/selection/", json=data, content_type='application/json')
    logger.debug(f"Response status code: {response.status_code}, Response data: {response.data}")
    selection_id = response.get_json()["id"]

    # Update the selection to inactive
    response = client.patch(f"/selection/{selection_id}", json={"active": False, "price":10})
    assert response.status_code == 200
    assert "id" in response.get_json()

# def test_delete_selection(client):
#     response = client.delete("/selection/1")
#     assert response.status_code == 200

def test_search_selection_by_name_regex(client):
    response = client.post("/selection/search", json={"name_regex": "Sel.*"})
    assert response.status_code == 200
    assert "selections" in response.get_json()

def test_search_selection_by_min_active(client):
    response = client.post("/selection/search", json={"min_active_selections": 1})
    assert response.status_code == 200
    assert "selections" in response.get_json()