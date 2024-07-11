class SportsValidator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_sports_data(data):
        if not data:
            return (400, "Body not provided correctly")

        if "name" not in data:
            return (400, "Name not present in body")

        if not isinstance(data["name"], str) or \
            not isinstance(data.get("slug", ""), str) or \
                not isinstance(data.get("active", False), bool):
            return (400, "Incorrect datatypes provided for one or more values")
        
        return (200, "Data looks good")

    @staticmethod
    def validate_sportid(sport_id):
        if not sport_id or not isinstance(sport_id, int):
            return (400, "Sport id provided is not a number")
        return (200, "Sport id looks good")

    @staticmethod
    def validate_sport_filters(data):
        # UNCOMMENT if search request body cant be empty

        # if not data:
        #     return (400, "Body not provided correctly")

        # if "name" not in data and "active" not in data:
        #     return (400, "Incorrect filters provided")

        if not isinstance(data.get("name",""), str) or \
            not isinstance(data.get("active", False), bool):
            return 400, "Incorrect datatypes provided for one or more values"

        if "min_active_events" in data != "sport" in data:
            return 400, "Incorrect filters provided, min_active_events should be paired with sport"
        
        if not isinstance(data.get("min_active_events", 0), int) or \
            not isinstance(data.get("sport", ""), str):
            return 400, "Incorrect datatypes provided for one or more values"
        
        return 200, "Filter data looks good"
        
class EventsValidator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_events_data(data, update=False):
        if not update and not data or ["name", "type", "sport", "status", "scheduled_start"] in list(data.keys()):
            return (400, "Body not provided correctly")

        if "status" in data and data["status"] not in ["PENDING", "STARTED", "ENDED", "CANCELLED"]:
            return (400, "Status value is not acceptable")
        
        if "type" in data and data["type"] not in ["preplay", "inplay"]:
            return (400, "Type value is not acceptable")
        
        if not isinstance(data.get("sport",""), str):
            return (400, "Sport should be a string")
        
        return (200, "Data looks good")

    @staticmethod
    def validate_eventid(event_id):
        if not event_id or not isinstance(event_id, int):
            return (400, "Event id provided is not a number")
        return (200, "Event id looks good")

    @staticmethod
    def validate_event_filters(data):
        if not data:
            return (400, "Body not provided correctly")

        if "name" not in data and "active" not in data:
            return (400, "Incorrect filters provided")

        if not isinstance(data["name"], str) or \
            not isinstance(data.get("active", False), bool):
            return (400, "Incorrect datatypes provided for one or more values")
    
        if "min_active_selections" in data != "event" in data:
            return 400, "Incorrect filters provided, min_active_events should be paired with sport"
        
        if not isinstance(data.get("min_active_selections", 0), int) or \
            not isinstance(data.get("event", ""), str):
            return 400, "Incorrect datatypes provided for one or more values"

        return (200, "Data looks good")
    
class SelectionsValidator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_selections_data(data):
        if not data or ["name", "event", "price", "outcome"] in list(data.keys()):
            return (400, "Body not provided correctly")

        # if not isinstance(data["name"], str) or \
        #     not isinstance(data.get("slug", ""), str) or \
        #         not isinstance(data.get("active", False), bool):
        #     return (400, "Incorrect datatypes provided for one or more values")
        
        return (200, "Data looks good")

    @staticmethod
    def validate_selectionid(selection_id):
        if not selection_id or not isinstance(selection_id, int):
            return (400, "Selection id provided is not a number")
        return (200, "Selection id looks good")

    @staticmethod
    def validate_selection_filters(data):
        if not data:
            return (400, "Body not provided correctly")

        if "name" not in data and "active" not in data:
            return (400, "Incorrect filters provided")

        if not isinstance(data.get("name",""), str) or \
            not isinstance(data.get("active", False), bool):
            return (400, "Incorrect datatypes provided for one or more values")
        
        return (200, "Data looks good")