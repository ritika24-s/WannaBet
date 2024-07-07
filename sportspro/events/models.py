from ..db import DB

class EventsModels(DB):
    def __init__(self):
        super().__init__()
    
    def create_event(self, data):
        query = "INSERT INTO events "\
                "(name, slug, active, type, sport, status, scheduled_start, actual_start, logos) "\
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (data['name'], data['slug'], data['active'], data['type'], 
                  data['sport'], data['status'], data['scheduled_start'], 
                  data['actual_start'], data['logos'])
        
        results = self.execute_query(query=query, values=values)
        return results

    def update_event(self, event_id, data):
        query = "UPDATE events SET name=%s, slug=%s, active=%s, type=%s, sport=%s, status=%s, scheduled_start=%s, actual_start=%s, logos=%s WHERE id=%s"
        values = (data['name'], data['slug'], data['active'], data['type'], data['sport'], data['status'], data['scheduled_start'], data['actual_start'], data['logos'], event_id)
        
        results = self.execute_query(query=query, values=values)
        return results

    def search_events(self, filters, fetchone=True):
        # cursor = self.connection.cursor(dictionary=True)
        results = self.select_data_where(select='*', table="events", 
                    where= ('name LIKE %' + filters['name'] + 'AND sport LIKE %' + filters['sport']),
                    fetchone=fetchone)
        return results
    
    def get_all_active_events(self):
        results = self.select_data_where(select="event_id", table="events", where="active=True", fetchone=False)
        return results
    
    def delete_event(self, event_id):
        results = None

        event_exists = self.select_data_where(select="id", table="events", where=f"id={event_id}")

        if event_exists:
            query = f"DELETE FROM events WHERE id={event_id};"
            results = self.execute_query(query=query)

        return results
