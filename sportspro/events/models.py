from ..db import DB

class EventsModels(DB):
    def __init__(self):
        super().__init__()
    
    def create_event(self, data):
        query = "INSERT INTO events "\
                "(name, slug, active, type, sport, status, scheduled_start, actual_start, logos) "\
                f"VALUES ({data['name']}, {data['slug']}, {data['active']}, , {data['type']}, "\
                f"{data['sport']}, {data['status']}, {data['scheduled_start']}, "\
                f"{data['actual_start']}), , {data['logos']}"
        results = self.execute_query(query=query)
        return results

    def update_event(self, event_id, data):
        query = "UPDATE events SET name=%s, slug=%s, active=%s, type=%s, sport=%s, status=%s, scheduled_start=%s, actual_start=%s, logos=%s WHERE id=%s" \
                %(data['name'], data['slug'], data['active'], data['type'], data['sport'], data['status'], data['scheduled_start'], data['actual_start'], data['logos'], event_id)
        self.execute_query(query=query)
        return event_id

    def search_events(self, filters):
        # cursor = self.connection.cursor(dictionary=True)
        results = self.select_data_where(select='*', table="events", 
                    where= ('name LIKE %' + filters['name'] + 'AND sport LIKE %' + filters['sport']),
                    fetchone=False)
        return results
    
    def get_all_active_events(self):
        results = self.select_data_where(select="event_id", table="events", where="active=True", fetchone=False)
        return results
