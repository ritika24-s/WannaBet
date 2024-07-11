from datetime import datetime

from .models import EventsModels
from ..utils.validators import EventsValidator
from ..utils.logger import get_logger

logger = get_logger(__name__)


class EventsViews:
    def __init__(self) -> None:
        self.events_db = EventsModels()

    @staticmethod
    def get_team_logo(team_name):
        import requests
        response = requests.get(f'https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team_name}')
        if response.status_code == 200:
            data = response.json()
            if data['teams']:
                return data['teams'][0]['strLogo']
        return ""

    def get_active_events_list(self):
        events = self.events_db.get_all_active_events()

    def check_event_exists(self, data):
        if "event_id" in data:
            filters = "id=%d" % (int(data["event_id"]))
        else:
            filters = "name='%s' AND sport='%s'" % (data["name"], data["sport"])
        
        return self.events_db.search_events(filters=filters)

    def get_events_data(self, results):
        """
        Get events dict from the provided search results.
        """
        events = []

        for result in results:
            event = {
                "id": result[0],
                "name": result[1],
                "slug": result[2],
                "active": bool(result[3]),
                "type": result[4],
                "sport": result[5],
                "status": result[6],
                "scheduled_start": result[7],
                "actual_start": result[8],
                "logos": result[9]
            }
            events.append(event)
        
        return events
    
    def create_event(self, data):
        logger.debug("Creating a new event with data: %s", data)

        status_code, message = EventsValidator.validate_events_data(data)

        if status_code != 200:
            logger.error("Validation failed for creating event: %s", message)
            return status_code, message
        
        if self.check_event_exists(data):
            logger.warning("Duplicate entry found for event: %s", data)
            return 409, "Duplicate entry"

        # format and gather the data needed before inserting into the database
        data['scheduled_start'] = datetime.strptime(data['scheduled_start'], "%Y-%m-%dT%H:%M:%SZ")
        
        if "actual_start" in data:
            data['actual_start'] = datetime.strptime(data['actual_start'], "%Y-%m-%dT%H:%M:%SZ")

        if not data.get("slug"):
            data["slug"] = data["name"].lower()

        team1, team2 = data["name"].split(" vs ")
        logo1 = EventsViews.get_team_logo(team1)
        logo2 = EventsViews.get_team_logo(team2)
        if not logo1 and not logo2:
             data["logos"] = None
        else:
            data["logos"] = f"{logo1}|{logo2}"

        event_id = self.events_db.create_event(data)

        if event_id:
            logger.info("Event created with ID: %d", event_id)
            return 201, event_id
        else:
            logger.error("Failed to create event: %s", data)
            return 500, "Internal Server Error"
    
    def update_event(self, event_id, data):
        """
        Update an existing event with the provided data.
        """
        logger.debug("Updating event ID %d with data: %s", event_id, data)

        status_code, message = EventsValidator.validate_eventid(event_id=event_id)
        if status_code != 200:
            logger.error("Validation failed for event data: %s", message)
            return status_code, message

        status_code, message = EventsValidator.validate_events_data(data=data)
        if status_code != 200:
            logger.error("Validation failed for data sent to be updated: %s", message)
            return status_code, message
        
        # check if the event exists and if yes then store it in a variable to capture the event name
        event = self.check_event_exists({"event_id": event_id})

        if event:
            if data.get("active") is None:
                # Check if the event should be marked as inactive
                data["active"] = self.events_db.check_event_active_status(event_name=event[0][1])
                print("active ", data["active"])

            # convert scheduled_start and actual start to datetime
            if "scheduled_start" in data and not isinstance(data["scheduled_start"], datetime):
                data['scheduled_start'] = datetime.strptime(data['scheduled_start'], "%Y-%m-%dT%H:%M:%SZ")
            
            if "actual_start" in data and not isinstance(data["actual_start"], datetime):
                data['actual_start'] = datetime.strptime(data['actual_start'], "%Y-%m-%dT%H:%M:%SZ")
            
            results = self.events_db.update_event(event_id=int(event_id), data=data)
            
            logger.debug(f"Value received after trying to update event - {results}")
            
            if results:
                logger.info("Event updated with ID: %d", event_id)
                return 200, event_id
            else:
                logger.error("Failed to update event ID %s: %s", event_id, data)
                return 500, "Something went wrong, check logs"
        
        return 400, f"Event with id {event_id} not found"

    def delete_event(self, event_id):
        status_code, message = EventsValidator.validate_eventid(event_id=event_id)
        if status_code != 200:
            return status_code, message
        
        if self.check_event_exists({"event_id":event_id}):
            results = self.events_db.delete_event(event_id=int(event_id))
            if results:
                return 200, event_id
            return 500, "Something went wrong, check logs"
        
        return 400, f"Event with id {event_id} not found"
    
    def search_events(self, data):
        """
        Search for events based on the provided filters.
        """
        logger.debug("Searching for events with filters: %s", data)
        status_code, message = EventsValidator.validate_event_filters(data)
        if status_code != 200:
            return status_code, message
        
        filters = "1=1"

        # Handling simple filters
        if 'slug' in data:
            filters += " AND slug LIKE '%" + data['slug'] + "%'"
        if 'active' in data:
            filters += f" AND active = {data['active']}"
        if 'type' in data:
            filters += f" AND type LIKE '%" + data['type'] + "%'"
        if 'sport' in data:
            filters += " AND sport like '%" + data["sport"] + "%'"
        if 'status' in data:
            filters += ' AND status=' + str(data['status'])
        if 'actual_start' in data:
            data["actual_start"]= datetime.strptime(data['actual_start'], "%Y-%m-%dT%H:%M:%SZ")
            filters += " AND actual_start = %s" % data['actual_start']
        if 'scheduled_start' in data:
            data["scheduled_start"]= datetime.strptime(data['scheduled_start'], "%Y-%m-%dT%H:%M:%SZ")
            filters += " AND scheduled_start = %s" % data['scheduled_start']
        if 'logos' in data:
            filters += " AND logos LIKE '%" + data["logos"] + "%'"

        # Regex filter for name
        if 'name_regex' in filters:
            filters += " AND name REGEXP '" + data['name_regex'] + "'"

        # Minimum number of active selections data
        if 'min_active_selections' in data and "event" in data:
            filters += " AND (SELECT COUNT(*) FROM selections WHERE event='%s' AND active = 1) >= %d" \
                        % (data["event"], data['min_active_events'])

        # Events scheduled to start in a specific timeframe
        if 'scheduled_start_from' in data and 'scheduled_start_to' in data:
            datetime.strptime(data['scheduled_start'], "%Y-%m-%dT%H:%M:%SZ")
            datetime.strptime(data['scheduled_start'], "%Y-%m-%dT%H:%M:%SZ")
            filters += " AND scheduled_start BETWEEN %s AND %s" \
                % (data['scheduled_start_from'], data['scheduled_start_to'])
            
        results = self.events_db.search_events(filters=filters, fetchone=False)
        
        if results:
            events = self.get_events_data(results=results)
            logger.info("Events found: %s", len(events))
            return 200, events
        
        logger.warning("No selection match the criteria: %s", data)
        return 404, "No event matches the criteria"
    
    def check_and_update_event_inactive_status(self, event_name):
        event_active_status = self.events_db.search_events(filters="name='%s' AND active=True" % event_name)
        all_selections_status = self.events_db.check_event_active_status(event_name=event_name)

        event_id = event_active_status[0][0]

        logger.info(f"Event: {event_name}, Event Status: {str(event_active_status)}, All Selections Status: {str(all_selections_status)}")
        
        if all_selections_status != event_active_status:
            logger.info(f"Changing the status of event {event_name} to {not all_selections_status}")

            results = self.events_db.update_event(event_id=event_id, data={"active":not all_selections_status})
            if results:
                logger.info("Event updated: %s", results)
                return 200, False
            
            logger.error("Failed to update event ID %d"% event_id)
            return 500, f"Failed to update event ID {event_id}"
        return 200, True

