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
                    data.get('actual_start'), data['logos'])
        
            results = self.execute_query(query=query, values=values)
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
        values = []
        results = None

        try:
            # Append fields to the query if they are provided in data
            if data.get('name'):
                query += "name = %s, "
                values.append(data['name'])
            if data.get("slug"):
                query += "slug = %s, "
                values.append(data['slug'])
            if data.get("active") is not None:
                query += "active = %s, "
                values.append(data['active'])
            if data.get("type") is not None:
                query += "type = %s, "
                values.append(data['type'])
            if data.get("sport") is not None:
                query += "sport = %s, "
                values.append(data['sport'])
            if data.get("status") is not None:
                query += "status = %s, "
                values.append(data['status'])
            if data.get("scheduled_start") is not None:
                query += "scheduled_start = %s, "
                values.append(data['scheduled_start'])
            if data.get("actual_start") is not None:
                query += "actual_start = %s, "
                values.append(data['actual_start'])
            if data.get("logos") is not None:
                query += "logos = %s, "
                values.append(data['logos'])

            if values:
                # Finalize the query with the WHERE clause
                query = query.rstrip(", ") + " WHERE id=%d"
                values.append(int(event_id))
        
                results = self.execute_query(query=query, values=tuple(values))
                if results:
                    logger.info(f"Event created successfully: {data['name']} with id:{results}")
                else:
                    logger.debug(f"No values returned after trying to update: ID {event_id}")
            else:
                logger.debug(f"No values provided to update: ID {event_id}")

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

        results = []

        try:
            # cursor = self.connection.cursor(dictionary=True)
            results = self.select_data_where(select='*', table="events", 
                        where= filters,
                        fetchone=fetchone)
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
