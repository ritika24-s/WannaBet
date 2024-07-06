import pytest

@pytest.fixture
def test_create_new_selection():
    selection = {
    "name": "Chelsea Win",
    "event": "Chelsea vs Manchester United",
    "price": 2.30,
    "active": True,
    "outcome": "UNSETTLED"
}

def test_update_selection():
    selection = {
    "name": "Chelsea Win",
    "event": "Chelsea vs Manchester United",
    "price": 2.30,
    "active": False,
    "outcome": "LOSE"
}

def test_search_selection():
    search = {
    "event": "Arsenal vs Leeds",
    "active": True
}
