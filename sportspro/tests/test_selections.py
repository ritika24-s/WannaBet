import pytest

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
