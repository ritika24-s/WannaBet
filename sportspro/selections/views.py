from .models import SelectionsModels
from ..utils.validators import SelectionsValidator
from ..utils.logger import get_logger

logger = get_logger("selection_views")


class SelectionsViews:
    def __init__(self) -> None:
        self.selections_db = SelectionsModels()

    def get_selection_list(self):
        pass

    def get_selections_data(self, results):
        """
        Get selections dict from the provided search results.
        """
        selections = []

        for result in results:
            selection = {
                "id": result[0],
                "name": result[1],
                "event_id": result[2],
                "active": bool(result[3]),
                "odds": result[4],
                "outcome": result[5]
            }
            selections.append(selection)
        
        return selections
        
    def check_selection_exists(self, data):
        if "selection_id" in data:
            filters = "id=%d" % (int(data["selection_id"]))
        else:
            filters = "name=%s AND event=%s" % (data["name"], data["event"])
        
        return self.selections_db.search_selections(filters=filters)

    def create_selection(self, data):
        status_code, message = SelectionsValidator.validate_selections_data(data)

        if status_code != 200:
            return status_code, message
        
        if self.check_selection_exists(data):
            return 409, "Duplicate entry"
        
        selection_id = self.selections_db.create_selection(data)
        if selection_id:
            return 201, selection_id
    
    def update_selection(self, selection_id, data):
        status_code, message = SelectionsValidator.validate_selectionid(selection_id=selection_id)
        if status_code != 200:
            return status_code, message
        
        status_code, message = SelectionsValidator.validate_selections_data(data)
        if status_code != 200:
            return status_code, message
        
        if self.check_selection_exists({"selection_id":selection_id}):
            results = self.selections_db.update_selection(selection_id=selection_id, data=data)
            
            if results:
                return 200, selection_id
            return 500, "Something went wrong, check logs"
        
        return 404, f"Selection with id {selection_id} not found"

    def delete_selection(self, selection_id):
        status_code, message = SelectionsValidator.validate_selectionid(selection_id=selection_id)
        if status_code != 200:
            return status_code, message
        
        if self.check_selection_exists({"selection_id":selection_id}):
            results = self.selections_db.delete_selection(selection_id=int(selection_id))
            if results:
                return 200, selection_id
            return 500, "Something went wrong, check logs"
        
        return 400, f"Selection with id {selection_id} not found"
    
    def search_selection(self, data):
        status_code, message = SelectionsValidator.validate_selection_filters(data)
        if status_code != 200:
            return status_code, message
        
        filters = "1=1"
        # not choosing the below written code because it might cause SQL data injection
        # filters = (" AND ").join(str(keys) + " LIKE %" + str(values) + "%" for keys, values in data.items())
        
        if data.get('event'):
            filters += " AND event like '%" + data["event"] + "%'"
        if data.get('active'):
            filters += ' AND active=' + str(data['active'])
        if data.get('outcome'):
            filters += ' AND outcome=' + str(data['outcome'])

        results = self.selections_db.search_selections(filters=filters)
        
        if results:
            selections = self.get_selections_data(results=results)
            logger.info("Selection found: %s", len(selections))
            return 200, selections
        
        logger.warning("No selection match the criteria: %s", data)
        return 404, "No selection matches the criteria"