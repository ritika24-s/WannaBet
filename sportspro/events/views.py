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
        

    def create_event(self, data):
        status_code, message = EventsValidator.validate_events_data(data)
        
        if status_code != 200:
            return status_code, message
        else:
            event_exists = self.events_db.search_events(filters="name='" + data["name"] + "'")
            
            if event_exists:
                return 409, "Duplicate entry"
            
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
        
        event_id = self.events_db.update_event(event_id=event_id, data=data)
        if event_id:
            return 200, event_id
        else:
            return 500, "Something went wrong, check logs"

    def delete_event(self, event_id):
        status_code, message = EventsValidator.validate_eventid(event_id=event_id)
        if status_code != 200:
            return status_code, message
        
        results = self.events_db.delete_event(event_id=int(event_id))
        if results:
            return 200, event_id
        
        return 400, "event doesnt exist"
    
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