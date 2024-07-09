from .models import SportsModels
from ..utils.validators import SportsValidator

from ..utils.logger import get_logger
logger = get_logger("sports_views")


class SportsViews:
    def __init__(self) -> None:
        self.sports_db = SportsModels()

    def get_sports_list(self):
        pass
    
    def check_sport_exists(self, data):
        """
        Check if a sport already exists based on the provided data.
        """
        if "sport_id" in data:
            filters = "id=%d" % (int(data["sport_id"]))
        else:
            filters = "name='%s'" % data["name"]
        
        return self.sports_db.search_sports(filters=filters)
    
    def get_data(self, data):
        """
        Extract sport data from the provided input.
        """
        name = data['name']
        slug = data.get('slug', "")
        active = data.get('active', True)
        return name, slug, active
    
    def create_sport(self, data):
        """
        Create a new sport with the provided data.
        """
        logger.debug("Creating a new sport with data: %s", data)

        status_code, message = SportsValidator.validate_sports_data(data)

        if status_code != 200:
            logger.error("Validation failed for creating sport: %s", message)
            return status_code, message
        else:
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
        
        status_code, message = SportsValidator.validate_sports_data(data)
        if status_code != 200:
            logger.error("Validation failed for sport data: %s", message)
            return status_code, message
        
        if self.check_sport_exists({"sport_id": sport_id}):
            sport_id = self.sports_db.update_sport(sport_id=sport_id, data=data)
            if sport_id:
                logger.info("Sport updated with ID: %d", sport_id)
                return 200, sport_id
            else:
                logger.error("Failed to update sport ID %d: %s", sport_id, data)
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
        if "name" in data:
            filters += " AND name LIKE '%%%s%%'" % data["name"]
        if "active" in data:
            filters += " AND active=%d" % data['active']

        results = self.sports_db.search_sports(filters=filters)
        if results:
            logger.info("Sports found: %s", results)
            return 200, results
        else:
            logger.warning("No sports match the criteria: %s", data)
            return 404, "No sport matches the criteria"