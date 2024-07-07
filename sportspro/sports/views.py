from .models import SportsModels
from ..utils.validators import SportsValidator

class SportsViews:
    def __init__(self) -> None:
        self.sports_db = SportsModels()
    def get_sports_list(self):
        pass

    def create_sport(self, data):
        status_code, message = validate_sports_data(data)
        print(status_code)
        if status_code != 200:
            return status_code, message
        else:
            sports_exists = self.sports_db.search_sports(filters="name='"+ data["name"]+ "'")
            
            if sports_exists:
                return 409, "Duplicate entry"
            
            sport_id = self.sports_db.create_sport(data)
            if sport_id:
                return 201, sport_id
        

    def update_sport(self, sport_id, data):
        status_code, message = SportsValidator.validate_sportid(sport_id=sport_id)
        if status_code != 200:
            return status_code, message
        
        status_code, message = SportsValidator.validate_sports_data(data)
        if status_code != 200:
            return status_code, message
        
        sport_id = self.sports_db.update_sport(sport_id=sport_id, data=data)
        if sport_id:
            return 200, sport_id
        else:
            return 500, "Something went wrong, check logs"

    def delete_sport(self, sport_id):
        status_code, message = SportsValidator.validate_sportid(sport_id=sport_id)
        if status_code != 200:
            return status_code, message
        
        results = self.sports_db.delete_sport(sport_id=int(sport_id))
        if results:
            return 200, sport_id
        
        return 400, "Sport doesnt exist"
    
    def search_sport(self, data):
        status_code, message = SportsValidator.validate_sport_filters(data)
        if status_code != 200:
            return status_code, message
        
        filters = "1=1"
        # not choosing the below written code because it might cause SQL data injection
        # filters = (" AND ").join(str(keys) + " LIKE %" + str(values) + "%" for keys, values in data.items())
        
        if "name" in data:
            filters += " AND name like '%" + data["name"] + "%'"
        if "active" in data:
            filters += ' AND active=' + str(data['active'])

        results = self.sports_db.search_sports(filters=filters)
        if results:
            return 200, results
        
        return 404, "No sport matches the criteria"