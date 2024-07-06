sports = [
    {
        "id": 1,
        "name": "Football",
        "slug": "football",
        "active": True
    },
    {
        "id": 2,
        "name": "Basketball",
        "slug": "basketball",
        "active": True
    },
    {
        "id": 3,
        "name": "Tennis",
        "slug": "tennis",
        "active": False
    }
]

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
