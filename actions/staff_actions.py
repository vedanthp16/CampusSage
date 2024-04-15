from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from bson import ObjectId

from actions.common import CorrectSpelling

client = MongoClient("mongodb://localhost:27017/")   
db = client.CampusSage


class ActionAskDepartmentStaff(Action):
    def name(self) -> str:
        return "action_department_staff"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Retrieve the department_name entity from the tracker
        department_name = None
        for entity in tracker.latest_message['entities']:
            if entity['entity'] == 'department_name':
                department_name = entity['value']
                break
        
        # Query the Departments collection to get the department information
        department = db.Departments.find_one({"DepartmentName": department_name})
        
        # Check if department was found
        if department:
            # Convert the department ObjectId to string to match the DepartmentId in the Staffs collection
            department_id_str = str(department["_id"])

            # Query the Staffs collection for staff members with the matching departmentId
            staff_members = db.Staffs.find({"DepartmentId": department_id_str})

            # Retrieve the names of the staff members
            staff_names = [staff["Name"] for staff in staff_members]
            
            # Construct a response listing the staff names
            if staff_names:
                response = f"The staff members in the {department_name} department are: " + ", ".join(staff_names) + "."
            else:
                response = f"There are no staff members found in the {department_name} department."
        else:
            response = f"I couldn't find information for the department '{department_name}'."
        
        # Send the response to the user
        dispatcher.utter_message(text=response)
        
        return []
