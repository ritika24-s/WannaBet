from .models import EventsModels
from ..utils.validators import EventsValidator

class EventsViews:
    def __init__(self) -> None:
        self.events_db = EventsModels()

    @staticmethod
    def get_team_logo(team_name):
        import requests
        response = requests.get(f'https://www.theEventsdb.com/api/v1/json/3/searchteams.php?t={team_name}')
        if response.status_code == 200:
            data = response.json()
            if data['teams']:
                return data['teams'][0]['strTeamBadge']
        return ""

    def get_active_events_list(self):
        events = self.events_db.get_all_active_events()

    def check_event_exists(self, data):
        if "event_id" in data:
            filters = "id=%d" % (int(data["event_id"]))
        else:
            filters = "name=%s AND sport=%s" % (data["name"], data["sport"])
        
        return self.events_db.search_events(filters=filters)

        
    def create_event(self, data):
        status_code, message = EventsValidator.validate_events_data(data)
        
        if status_code != 200:
            return status_code, message
        
        if self.check_event_exists(data):
            return 409, "Duplicate entry"

        if not data.get("slug"):
            data["slug"] = ""
        team1, team2 = data["name"].split(" vs ")
        logo1 = EventsViews.get_team_logo(team1)
        logo2 = EventsViews.get_team_logo(team2)
        data["logos"] = f"{logo1}|{logo2}"

        event_id = self.events_db.create_event(data)
        if event_id:
            return 201, event_id
    
    def update_event(self, event_id, data):
        status_code, message = EventsValidator.validate_eventid(event_id=event_id)
        if status_code != 200:
            return status_code, message
        
        status_code, message = EventsValidator.validate_events_data(data)
        if status_code != 200:
            return status_code, message
        
        if self.check_event_exists({"event_id":event_id}):
            results = self.events_db.update_event(event_id=int(event_id), data=data)
            if results:
                return 200, event_id
            return 500, "Something went wrong, check logs"
        
        return 400, f"Event with id {event_id} not found"

    def delete_event(self, event_id):
        status_code, message = EventsValidator.validate_eventid(event_id=event_id)
        if status_code != 200:
            return status_code, message
        
        if self.check_event_exists({"event_id":event_id}):
            results = self.events_db.delete_event(event_id=int(event_id))
            if results:
                return 200, event_id
            return 500, "Something went wrong, check logs"
        
        return 400, f"Event with id {event_id} not found"
    
    def search_events(self, data):
        status_code, message = EventsValidator.validate_event_filters(data)
        if status_code != 200:
            return status_code, message
        
        filters = "1=1"

        if data.get('sport'):
            filters += " AND sport like '%" + data["sport"] + "%'"
        if data.get('status'):
            filters += ' AND status=' + str(data['status'])

        results = self.events_db.search_events(filters=filters, fetchone=False)
        if results:
            return 200, results
        
        return 404, "No event matches the criteria"