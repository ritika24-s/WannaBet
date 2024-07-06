import pytest

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
