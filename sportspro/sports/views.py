from .models import SportsModels
from ..utils.validators import SportsValidator

from ..utils.logger import get_logger
logger = get_logger("sports_views")


class SportsViews:
    def __init__(self) -> None:
        self.sports_db = SportsModels()

    def get_sports_list(self):
        """
        Retrieve a list of all sports.
        """
        return self.sports_db.get_sports_list()
    
    def check_sport_exists(self, data):
        """
        Check if a sport already exists based on the provided data.
        """
        if "sport_id" in data:
            filters = "id=%d" % (int(data["sport_id"]))
        else:
            filters = "name='%s'" % data["name"]
        
        return self.sports_db.search_sports(filters=filters)
    
    def get_data(self, results):
        """
        Get sport dict from the provided search results.
        """
        sports = []

        for result in results:
            sport = {
                "id": result[0],
                "name": result[1],
                "slug": result[2],
                "active": bool(result[3])
            }
            sports.append(sport)

        return sports
    
    def create_sport(self, data):
        """
        Create a new sport with the provided data.
        """
        logger.debug("Creating a new sport with data: %s", data)

        status_code, message = SportsValidator.validate_sports_data(data)

        if status_code != 200:
            logger.error("Validation failed for creating sport: %s", message)
            return status_code, message
        
        if self.check_sport_exists(data=data):
            logger.warning("Duplicate entry found for sport: %s", data)
            return 409, "Duplicate entry"
        
        sport_id = self.sports_db.create_sport(name=data['name'],
                                                slug=data.get('slug'),
                                                active=data.get('active', True))
        if sport_id:
            logger.info("Sport created with ID: %d", sport_id)
            return 201, sport_id
        else:
            logger.error("Failed to create sport: %s", data)
            return 500, "Internal Server Error"
        
    def update_sport(self, sport_id, data):
        """
        Update an existing sport with the provided data.
        """
        logger.debug("Updating sport ID %d with data: %s", sport_id, data)
        
        status_code, message = SportsValidator.validate_sportid(sport_id=sport_id)
        if status_code != 200:
            logger.error("Validation failed for sport data: %s", message)
            return status_code, message
        
        # check if the sport exists and if yes then store it in a variable to capture the sport name
        sport = self.check_sport_exists({"sport_id": sport_id})

        if sport:
            if data.get("active") is None:
                # Check if the sport should be marked as inactive
                data["active"] = self.sports_db.check_sport_active_status(sport_name=sport[0][1])
                
            sport_id = self.sports_db.update_sport(sport_id=sport_id, data=data)
            
            logger.debug(f"Value received after trying to update sport - {sport_id}")
            
            if sport_id:
                logger.info("Sport updated with ID: %d", sport_id)
                return 200, sport_id
            else:
                logger.error("Failed to update sport ID %s: %s", sport_id, data)
                return 500, "Something went wrong, check logs"
        
        else:
            logger.warning("Sport with ID %d not found", sport_id)
            return 404, f"Sport with id {sport_id} not found"

    def delete_sport(self, sport_id, data):
        """
        Delete an existing sport by ID.
        """
        logger.debug("Deleting sport ID %d with data: %s", sport_id, data)
        status_code, message = SportsValidator.validate_sportid(sport_id=sport_id)
        if status_code != 200:
            logger.error("Validation failed for sport ID %d: %s", sport_id, message)
            return status_code, message

        if "name" in data:
            sport_exists = self.check_sport_exists(data)
            field = "name"
            value = data["name"]
        else:
            sport_exists = self.check_sport_exists({"sport_id": sport_id})
            field = "id"
            value = sport_id
        
        if sport_exists:
            results = self.sports_db.delete_sport(field, value)
            logger.info("Sport deleted with %s: %s", field, value)
            return 200, sport_id
        else:
            logger.warning("Sport with ID %d does not exist", sport_id)
            return 404, "Sport doesn't exist"

    def search_sport(self, data):
        """
        Search for sports based on the provided filters.
        """
        logger.debug("Searching for sports with filters: %s", data)

        status_code, message = SportsValidator.validate_sport_filters(data)
        if status_code != 200:
            logger.error("Validation failed for search filters: %s", message)
            return status_code, message
        
        filters = "1=1"
        # manually checking filters to avoid SQL injection issues
        if "name" in data:
            filters += " AND name like '%" + data["name"] + "%'"
        if "active" in data:
            filters += " AND active=%d" % data['active']
        if 'name_regex' in filters:
            filters += " AND name REGEXP '" + data["name_regex"] + "'"
        if 'min_active_events' in filters:
            filters += " AND (SELECT COUNT(*) FROM events WHERE sport='%s' AND active=True) >= %d" \
            % (data["sport"], data['min_active_events'])
        
        results = self.sports_db.search_sports(filters=filters, fetchone=False)
        if results:
            sports = self.get_data(results=results)
            logger.info("Sports found: %s", len(sports))
            return 200, sports

        logger.warning("No sports match the criteria: %s", data)
        return 404, "No sport matches the criteria"
    
    def check_and_update_sport_inactive_status(self, sport_name):
        sport_active_status = self.sports_db.search_sports(filters="name='%s' AND active=True" % sport_name, fetchone=True)
        all_events_status = self.sports_db.check_sport_active_status(sport_name=sport_name)

        sport_id = sport_active_status[0][0]
        
        logger.info(f"Sport: {sport_name}, Sport Status: {str(sport_active_status)}, All Events Status: {str(all_events_status)}")
        
        if all_events_status != sport_active_status:
            logger.info(f"Changing the status of {sport_name} to {not all_events_status}")
        
            results = self.update_sport(sport_id=sport_active_status[0][0], data={"active":not all_events_status})
            if results:
                logger.info("Sports updated: %s", results)
                return 200, False
            
            logger.error("Failed to update sport ID %d"% sport_id)
            return 500, f"Failed to update sport ID {sport_id}"
        return 200, True

