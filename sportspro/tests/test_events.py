import pytest

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
