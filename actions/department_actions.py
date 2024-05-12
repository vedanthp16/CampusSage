from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from bson import ObjectId

from actions.common import CorrectSpelling

client = MongoClient("mongodb://localhost:27017/")   
db = client.CampusSage  

class ActionAskDepartmentHod(Action):
    def name(self) -> str:
        return "action_department_hod"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Retrieve the department_name entity from the tracker
        department_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'department_name':
                department_name = entity['value']
                break
        
        # Query the Departments collection for the department information
        department = db.Departments.find_one({"DepartmentName": department_name})
        
        # If department is found, proceed to find the HOD
        if department:
            hod_id = department["HODId"]
            # Query the Staffs collection to find the HOD name
            if hod_id:
                hod = db.Staffs.find_one({"_id": ObjectId(hod_id)})
                if hod:
                    hod_name = hod["Name"]
                    response = f"The head of the {department_name} department is {hod_name}."
                else:
                    response = f"I couldn't find the head of the {department_name} department."
            else:
                response = f"The {department_name} department does not have a specified head."
        else:
            response = f"I couldn't find information for the department '{department_name}'."
        
        # Send the response to the user
        dispatcher.utter_message(text=response)
        return []

class ActionAskDepartmentVision(Action):
    def name(self) -> str:
        return "action_department_vision"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Retrieve the department_name entity from the tracker
        department_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'department_name':
                department_name = entity['value']
                break
        print(department_name)
        # Query the Departments collection for the department information
        department = db.Departments.find_one({"DepartmentName": department_name})
        
        # If department is found, respond with the vision
        if department:
            vision = department["Vision"]
            response = f"The vision of the {department_name} department is: {vision}."
        else:
            response = f"I couldn't find information for the department '{department_name}'."
        
        # Send the response to the user
        dispatcher.utter_message(text=response)
        return []

class ActionAskDepartmentMission(Action):
    def name(self) -> str:
        return "action_department_mission"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Retrieve the department_name entity from the tracker
        department_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'department_name':
                department_name = entity['value']
                break
        
        # Query the Departments collection for the department information
        department = db.Departments.find_one({"DepartmentName": department_name})
        
        # If department is found, respond with the motto
        if department:
            motto = department.get("Mission")
            response = f"The mission of the {department_name} department is: {motto}."
        else:
            response = f"I couldn't find information for the department '{department_name}'."
        
        # Send the response to the user
        dispatcher.utter_message(text=response)
        return []

class ActionAskDepartmentFullInfo(Action):
    def name(self) -> str:
        return "action_department_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Retrieve the department_name entity from the tracker
        department_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'department_name':
                department_name = entity['value']
                break
        
        # Query the Departments collection for the department information
        department = db.Departments.find_one({"DepartmentName": department_name})
        
        # If department is found, gather the necessary information
        if department:
            vision = department["Vision"]
            motto = department["Mission"]
            established_year = department["EstablishedYear"]
            hod_id = department["HODId"]
            
            # Query the Staffs collection to find the HOD name
            hod_name = None
            if hod_id:
                hod = db.Staffs.find_one({"_id": ObjectId(hod_id)})
                if hod:
                    hod_name = hod["Name"]

            # Construct the response
            response = f"The {department_name} department was established in {established_year}. " \
                       f"Its vision is: {vision}. Its mission is: {motto}."
            
            # Add HOD name if found
            if hod_name:
                response += f" The head of the department is {hod_name}."
            
            # Send the response to the user
            dispatcher.utter_message(text=response)
        else:
            response = f"I couldn't find information for the department '{department_name}'."
            dispatcher.utter_message(text=response)
        
        return []

class ActionAskDepartmentEstablishedYear(Action):
    def name(self) -> str:
        return "action_department_year"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Retrieve the department_name entity from the tracker
        department_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'department_name':
                department_name = entity['value']
                break
        
        # Query the Departments collection for the department information
        department = db.Departments.find_one({"DepartmentName": department_name})
        
        # If department is found, respond with the established year
        if department:
            established_year = department["EstablishedYear"]
            response = f"The {department_name} department was established in {established_year}."
            dispatcher.utter_message(text=response)
        else:
            response = f"I couldn't find information for the department '{department_name}'."
            dispatcher.utter_message(text=response)
        
        return []

