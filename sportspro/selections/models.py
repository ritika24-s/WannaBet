from ..db import DB

class SelectionsModels(DB):
    def __init__(self):
        super().__init__()

    def create_selection(self, data):
        query = "INSERT INTO selections (name, event, active, price, outcome) VALUES (%s, %s, %s, %s, %s)" % (data['name'], data['event'], data['active'], data['price'], data['outcome'])
        results = self.execute_query(query=query)
        return results

    def update_selection(self, selection_id, data):
        query = "UPDATE selections SET name=%s, event=%s, active=%s, price=%s, outcome=%s WHERE id=%s" % (data['name'], data['event'], data['active'], data['price'], data['outcome'], selection_id)
        results = self.execute_query(query=query)
        return results

    def search_selections(self, filters):
        # cursor = self.connection.cursor(dictionary=True)
        results = self.select_data_where(select="*", table="selections",
                    where = ('name LIKE %' + filters['name'] + ' AND event LIKE %' + filters['event']),
                    fetchone=False)
        return results
    
    # def check_is_event_active(self):
