from .models import EventsModels

class EventsViews:
    def __init__(self) -> None:
        self.events_db = EventsModels()

    def get_active_events_list(self):
        events = self.events_db.get_all_active_events()
        

    def create_event(self, data):
        if ["name", "type", "sport", "status", "scheduled_start"] in data.keys():
            self.events_db.create_event(data)