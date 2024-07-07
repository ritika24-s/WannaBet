from .models import SelectionsModels

class SelectionsViews:
    def __init__(self) -> None:
        self.selections_db = SelectionsModels()

    def get_selection_list(self):
        pass

    def create_selection(self, data):
        if ["name", "event", "price", "outcome"] in data.keys():
            self.selections_db.create_selection(data)