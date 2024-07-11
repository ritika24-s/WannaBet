from ..db import DB
from ..utils.logger import get_logger

logger = get_logger('events_models')


class EventsModels(DB):
    def __init__(self):
        super().__init__()
    
    def create_event(self, data):
        """
        Create a new event in the database.

        Parameters:
        data (dict): Dictionary containing event details.

        Returns:
        int: ID of the created event if successful, None otherwise.
        """
        logger.debug(f"Creating event with name: {data['name']} for sport: {data['sport']}")
        results = None
        
        try:
            query = "INSERT INTO events "\
                    "(name, slug, active, type, sport, status, scheduled_start, actual_start, logos) "\
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (data['name'], data.get("slug", ""), data.get('active', False), data['type'],
                    data['sport'], data['status'], data['scheduled_start'],
                    data.get('actual_start'), data.get('logos'))
        
            results = self.execute_query(query=query, values=values, insert=True)
            if results:
                logger.info(f"Event created successfully: {data['name']} with id:{results}")
            else:
                logger.debug(f"No values returned after trying to create: {data['name']}")
        
        except Exception as e:
            logger.error(f"Error creating event: {e}")
        finally:
            return results

    def update_event(self, event_id, data):
        """
        Update an existing event in the database.

        Parameters:
        event_id (int): ID of the event to be updated.
        data (dict): Dictionary containing updated event details.

        Returns:
        int: ID of the updated event if successful, None otherwise.
        """
        logger.debug(f"Updating event with ID: {event_id}")

        query = "UPDATE events SET "
        query_parts = []
        results = 0

        try:
            # Append fields to the query if they are provided in data           
            if data.get("scheduled_start") is not None:
                query_parts.append("scheduled_start = " + data['scheduled_start'])
            if data.get("actual_start") is not None:
                query_parts.append("actual_start = " + data['actual_start'])
            if "name" in data:
                query_parts.append("name = '%" + data["name"] + "%'")
            if "slug" in data:
                query_parts.append("slug = '%" + data["slug"] + "%'")
            if "active" in data:
                query_parts.append("active = " + str(data["active"]))
            if "type" in data:
                query_parts.append("type = '%" + data["type"] + "%'")
            if "sport" in data:
                query_parts.append("sport = '%" + data["sport"] + "%'")
            if "status" in data:
                query_parts.append("status = '%" + data["status"] + "%'")
            if "logos" in data:
                query_parts.append("logos = '%" + data["logos"] + "%'")

            if query_parts:
                query += ", ".join(query_parts) + " WHERE id = %d" % event_id
            
            logger.debug(f"Query: {query}")
            results = self.execute_query(query=query)
            if results:
                logger.info(f"Event updated successfully with id:{event_id}")
            else:
                logger.debug(f"No values returned after trying to update: ID {event_id}")

        except Exception as e:
            logger.error(f"Error updating event: {e}")
        finally:
            return results

    def search_events(self, filters, fetchone=True):
        """
        Search for events in the database based on filters.

        Parameters:
        filters (dict): Dictionary containing search filters.
        fetchone (bool): Whether to fetch only one result.

        Returns:
        list: List of events matching the search criteria.
        """
        logger.debug(f"Searching for events with filters: {filters}")

        try:
            # cursor = self.connection.cursor(dictionary=True)
            result = self.select_data_where(select='*', table="events", 
                        where= filters,
                        fetchone=fetchone)
            
            if fetchone:
                results = [result] if result else []
            else:
                results = result

            logger.info(f"Found {len(results)} events matching criteria")

        except Exception as e:
            logger.error(f"Error searching events: {e}")
        finally:
            return results
    
    def get_all_active_events(self):
        """
        Get all active events.

        Returns:
        list: List of IDs of all active events.
        """
        results = self.select_data_where(select="event_id", table="events", where="active=True", fetchone=False)
        return results
    
    def delete_event(self, event_id):
        """
        Delete an event from the database.

        Parameters:
        event_id (int): ID of the event to be deleted.

        Returns:
        int: ID of the deleted event if successful, None otherwise.
        """
        try:
            # Execute the delete query
            query = f"DELETE FROM events WHERE id={event_id};"
            results = self.execute_query(query=query)
            logger.info(f"Event deleted successfully: ID {event_id}")
        except Exception as e:
            logger.error(f"Error deleting event: {e}")
        finally:
            return results
        
    def check_event_active_status(self, event_name):
        """
        Check if all selections of a event are inactive
        """
        active = True
        
        logger.debug(f"Checking inactive status for event: {event_name}")
        try:
            # query = "SELECT COUNT(*) FROM selections WHERE event=%s AND active=1"
            filters = f"event='{event_name}' AND active=True"
            active_selection_count = self.select_data_where(select='COUNT(*)', table="selections", where=filters)
            
            logger.debug(f"Active selections found for {event_name} = {active_selection_count[0]}")

            if active_selection_count[0] == 0:
                logger.info(f"Event {event_name} should be marked as inactive due to no active selections")
                active = False
        
        except Exception as e:
            logger.error(f"Error checking event inactive status: {e}")
        finally:
            return active


