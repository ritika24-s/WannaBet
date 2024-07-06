from .models import SportsModels

class SportsViews:
    def __init__(self) -> None:
        self.sports_db = SportsModels()
    def get_sports_list(self):
        pass

    def create_sport(self, data):
        if data.get("name"):
            sport_id, status = self.sports_db.create_sport(data)
        else:
            sport_id, status = "", 401
        
        return sport_id, status

    def update_sport(self, sport_id, data):
        pass