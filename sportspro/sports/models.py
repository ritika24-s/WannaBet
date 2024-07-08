from ..db import DB
from ..utils.logger import get_logger

logger = get_logger('sports_models')


class SportsModels(DB):
    def __init__(self):
        super().__init__()
    
    def check_schema(self):
        pass

    def create_sport(self, name, slug, active):
        logger.debug(f"Creating sport with name: {name}, slug: {slug}, active: {active}")

        query = "INSERT INTO sports (name, slug, active) VALUES (%s, %s, %s);"
        values = (name, slug, active)
        results = None
        try:
            results = self.execute_query(query=query, values=values)
            if results:
                logger.info(f"Sport created successfully: {name} and id {results}")
            else:
                logger.debug(f"No values returned after trying to create: {name}")
                
        except Exception as e:
            logger.error(f"Error creating sport: {e}")
        finally:
            return results
    
    def update_sport(self, sport_id, data):
        logger.debug(f"Updating sport with ID: {sport_id}")

        query = "UPDATE sports SET "
        values = []
        results = None

        try:
            if data.get('name'):
                query += "name = %s"
                values.append(data['name'])
            if data.get("slug"):
                query += "slug = %s"
                values.append(data['slug'])
            if data.get("active") is not None:
                query += "active = %s"
                values.append(data['active'])

            if values:
                query += "WHERE id=%d"
                values.append(int(sport_id))

                results = self.execute_query(query=query, values=values)
                if results:
                    logger.info(f"Sport updated successfully: ID {sport_id}")
                else:
                    logger.debug(f"No values returned after trying to update: ID {sport_id}")
            else:
                logger.debug(f"No values provided to update: ID {sport_id}")
        
        except Exception as e:
            logger.error(f"Error updating sport: {e}")
        
        finally:
            return results

    def search_sports(self, filters, fetchone=True):
        logger.debug(f"Searching for sports with filters: {filters}")
        results = []
        try:
            # cursor = self.connection.cursor(dictionary=True)
            results = self.select_data_where(select="*", table="sports",
                                where=filters,
                                fetchone=fetchone)
            logger.info(f"Found {len(results)} sports matching criteria")
            
        except Exception as e:
            logger.error(f"Error searching sports: {e}")
        finally:
            return results
    
    def delete_sport(self, field, value):
        results = None
        logger.debug(f"Deleting sports with {field}: {value}")

        try:
            if field == "name":
                query = f"DELETE FROM sports WHERE name='{value}';"
            else:
                query = f"DELETE FROM sports WHERE id={value};"
            print(query, field, value)
            results = self.execute_query(query=query)

            if results:
                logger.info(f"Sport deleted successfully with {field}: {value}")
            else:
                logger.debug(f"No values returned after trying to delete {field}: {value}")
            
        except Exception as e:
            logger.error(f"Error searching sports: {e}")
        finally:
            return results