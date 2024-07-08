from ..db import DB
from ..utils.logger import get_logger

logger = get_logger('selections_models')


class SelectionsModels(DB):
    # def __init__(self):
    #     super().__init__()

    def create_selection(self, data):
        logger.debug(f"Creating selection with name: {data['name']} for event: {data['event']}")

        results = None
        
        try:
            query = "INSERT INTO selections (name, event, active, price, outcome) VALUES (%s, %s, %s, %s, %s)" 
            values = (data['name'], data['event'], data.get('active', False), data['price'], data['outcome'])

            results = self.execute_query(query=query, values=values)
            if results:
                logger.info(f"Selection created successfully: {data['name']} with id:{results} for event: {data['event']}")
            else:
                logger.debug(f"No values returned after trying to create: {data['name']}")
        except Exception as e:
            logger.error(f"Error creating selection: {e}")
        finally:
            return results

    def update_selection(self, selection_id, data):
        logger.debug(f"Updating selection with ID: {selection_id} for event: {data['event']}")

        query = "UPDATE selections SET "
        values = []
        results = None
        
        try:
            if data.get('name'):
                query += "name = %s"
                values.append(data['name'])
            if data.get("event"):
                query += "event = %s"
                values.append(data['event'])
            if data.get("active") is not None:
                query += "active = %s"
                values.append(data['active'])
            if data.get("price") is not None:
                query += "price = %s"
                values.append(data['price'])
            if data.get("outcome") is not None:
                query += "outcome = %s"
                values.append(data['outcome'])

            if values:
                query += "WHERE id=%d"
                values.append(int(selection_id))

                results = self.execute_query(query=query, values=values)
                if results:
                    logger.info(f"Selection created successfully: {data['name']} with id:{results}")
                else:
                    logger.debug(f"No values returned after trying to update: ID {selection_id}")
            else:
                logger.debug(f"No values provided to update: ID {selection_id}")
            
        except Exception as e:
            logger.error(f"Error updating selection: {e}")
        finally:
            return results

    def search_selections(self, filters, fetchone=True):
        logger.debug(f"Searching for selections with filters: {filters}")

        results = []

        try:
            # cursor = self.connection.cursor(dictionary=True)
            results = self.select_data_where(select="*", table="selections",
                                            where=filters,
                                            fetchone=fetchone)
            logger.info(f"Found {len(results)} events matching criteria")

        except Exception as e:
            logger.error(f"Error searching events: {e}")
        finally:
            return results
    
    # def check_is_event_active(self):

    def delete_selection(self, selection_id):
        results = None

        selection_exists = self.select_data_where(select="id", table="selections", where=f"id={selection_id}",fetchone=True)
        if selection_exists:
            query = f"DELETE FROM selections WHERE id={selection_id};"
            results = self.execute_query(query=query)
        
        return results