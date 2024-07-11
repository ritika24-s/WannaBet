from ..db import DB
from ..utils.logger import get_logger

logger = get_logger('sports_models')


class SportsModels(DB):
    def __init__(self):
        super().__init__()
    
    def check_schema(self):
        pass

    def create_sport(self, name, slug, active):
        """
        Create a new sport in the database.
        """
        logger.debug(f"Creating sport with name: {name}, slug: {slug}, active: {active}")

        query = "INSERT INTO sports (name, slug, active) VALUES (%s, %s, %s);"
        values = (name, slug, active)
        results = None
        try:
            results = self.execute_query(query=query, values=values, insert=True)
            if results:
                logger.info(f"Sport created successfully: {name} with ID {results}")
            else:
                logger.debug(f"No values returned after trying to create: {name}")
                
        except Exception as e:
            logger.error(f"Error creating sport: {e}")
        finally:
            return results
    
    def update_sport(self, sport_id, data):
        """
        Update an existing sport in the database.
        """
        logger.debug(f"Updating sport with ID: {sport_id}")

        query = "UPDATE sports SET "
        values = []
        results = 0

        try:
            if 'name' in data:
                query += "name = %s, "
                values.append(data['name'])
            if 'slug' in data:
                query += "slug = %s, "
                values.append(data['slug'])
            if 'active' in data:
                query += "active = %s, "
                values.append(data['active'])

            # Remove the last comma and space
            query = query.rstrip(', ')
            query += " WHERE id=%s"
            values.append(int(sport_id))

            results = self.execute_query(query=query, values=tuple(values))
            if results:
                logger.info(f"Sport updated successfully: ID {sport_id}")
            else:
                logger.debug(f"No values returned after trying to update: ID {sport_id}")
        
        except Exception as e:
            logger.error(f"Error updating sport: {e}")
        finally:
            return results

    def search_sports(self, filters, fetchone=True):
        """
        Search for sports in the database based on provided filters.
        """
        logger.debug(f"Searching for sports with filters: {filters}")

        try:
            # cursor = self.connection.cursor(dictionary=True)
            result = self.select_data_where(select="*", table="sports",
                                where=filters,
                                fetchone=fetchone)
            
            if fetchone:
                results = [result] if result else []
            else:
                results = result
            logger.info(f"Found {len(results)} sports matching criteria - {results}")

        except Exception as e:
            logger.error(f"Error searching sports: {e}")
        finally:
            return results

    def delete_sport(self, field, value):
        """
        Delete a sport from the database based on the provided field and value.
        """
        results = None
        logger.debug(f"Deleting sports with {field}: {value}")
        query = f"DELETE FROM sports WHERE {field}={value};"
        try:
            results = self.execute_query(query=query)
            if results:
                logger.info(f"Sport deleted successfully with {field}: {value}")
            else:
                logger.debug(f"No values returned after trying to delete {field}: {value}")
            
        except Exception as e:
            logger.error(f"Error deleting sport: {e}")
        finally:
            return results

    def get_sports_list(self):
        """
        Retrieve a list of all sports from the database.
        """
        logger.debug("Retrieving all sports from the database")
        results = []
        try:
            results = self.select_data_where(select="*", table="sports", where="1=1", fetchone=False)
            logger.info(f"Found {len(results)} sports in total")
        except Exception as e:
            logger.error(f"Error retrieving sports: {e}")
        finally:
            return results
        
    def check_sport_active_status(self, sport_name):
        """
        Check if all events of a sport are inactive
        """
        active = True
        logger.debug(f"Checking inactive status for : {sport_name}")
        try:
            # query = "SELECT COUNT(*) FROM events WHERE sport=%s AND active=1"
            filters = f"sport='{sport_name}' AND active=True"
            active_event_count = self.select_data_where(select='COUNT(*)', table="events", where=filters)
            
            logger.debug(f"Active events found for {sport_name} = {active_event_count[0]}")

            if active_event_count[0] == 0:
                logger.info(f"Sport {sport_name} should be marked as inactive due to no active events")
                active = False
        
        except Exception as e:
            logger.error(f"Error checking sport inactive status: {e}")
        finally:
            return active

