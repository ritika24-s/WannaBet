from ..db import DB


class SportsModels(DB):
    def __init__(self):
        super().__init__()
    
    def check_schema(self):
        pass

    def create_sport(self, data):
        query = f"INSERT INTO sports (name, slug, active) VALUES \
        ({data['name']}, {data['slug']}, {data['active']})"
        results = self.execute_query(query=query)
        return results
    
    def update_sport(self, sport_id, data):
        query = "UPDATE sports SET name=%s, slug=%s, active=%s WHERE id=%s"\
                %(data['name'], data['slug'], data['active'], sport_id)
        results = self.execute_query(query=query)
        return results

    def search_sports(self, filters):
        # cursor = self.connection.cursor(dictionary=True)
        results = self.select_data_where(select="*", table="sports",
                               where=('name LIKE % ' + filters['name'] + 'AND active=', filters['active']),
                               fetchone=False)
        return results