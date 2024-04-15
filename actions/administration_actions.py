from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from bson import ObjectId

from actions.common import CorrectSpelling

client = MongoClient("mongodb://localhost:27017/")   
db = client.CampusSage


class ActionFindPersonByPosition(Action):
    def name(self) -> str:
        return "action_person_of_position"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) :
        # Connect to MongoDB (adjust the URI if necessary)

        # Retrieve the position entity from the tracker
        position_entity = None
        for entity in tracker.latest_message.get("entities", []):
            if entity["entity"] == "position":
                position_entity = entity["value"]
                break
        
        if not position_entity:
            dispatcher.utter_message(text="I couldn't understand the position you are asking about.")
            return []

        # Query the Administration collection to find the person holding the specified position
        result = db.Administration.find_one({"Position": position_entity})

        if result:
            person_name = result["Name"]
            dispatcher.utter_message(f"The person holding the position of {position_entity} is {person_name}.")
        else:
            dispatcher.utter_message(f"There is no one currently holding the position of {position_entity}.")

        return []
