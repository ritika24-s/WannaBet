from ..db import DB


class SportsModels(DB):
    def __init__(self):
        super().__init__()
    
    def check_schema(self):
        pass

    def create_sport(self, data):
        query = "INSERT INTO sports (name, slug, active) VALUES (%s, %s, %s);"
        values = (data['name'], data.get('slug',''), data.get('active', True))

        results = self.execute_query(query=query, values=values)
        return results
    
    def update_sport(self, sport_id, data):
        query = "UPDATE sports SET name=%s, slug=%s, active=%s WHERE id=%s"\
                %(data['name'], data['slug'], data['active'], sport_id)
        results = self.execute_query(query=query)
        return results

    def search_sports(self, filters, fetchone=False):
        # cursor = self.connection.cursor(dictionary=True)
        results = self.select_data_where(select="*", table="sports",
                               where=filters,
                               fetchone=fetchone)
        return results
    
    def delete_sport(self, sport_id):
        results = None

        sport_exists = self.select_data_where(select="id", table="sports", where=f"id={sport_id}",fetchone=True)
        if sport_exists:
            query = f"DELETE FROM sports WHERE id={sport_id};"
            print(query)
            results = self.execute_query(query=query)
        return results