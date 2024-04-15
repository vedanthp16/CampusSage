from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from bson import ObjectId

from actions.common import CorrectSpelling

client = MongoClient("mongodb://localhost:27017/")   
db = client.CampusSage


class ActionCourseDepartment(Action):
    def name(self) -> str:
        return "action_course_department"
    def run(self,dispatcher : CollectingDispatcher,tracker : Tracker,domain :dict):
        course_name = tracker.latest_message['entities'][0]['value']
        print(course_name)

        possible_course_names = [course["CourseName"] for course in db.Courses.find({},{"CourseName" : 1,"_id" : 0})]
        
        corrected_course_name = CorrectSpelling(course_name, possible_course_names)
        print(corrected_course_name)
        course = db.Courses.find_one({"CourseName": corrected_course_name})
        
        department_id = course["DepartmentId"]
        department_obj = ObjectId(department_id)
        department = db.Departments.find_one({"_id" : department_obj})

        if department:
            department_name = department.get("DepartmentName", "Unknown Department")
            response = f"The course {course['CourseName']} is offered by the {department_name} Department."
        else:
            response = f"Sorry, I couldn't find details for the department with ID {department_id}."
        dispatcher.utter_message(text=response)
        return []    

class ActionCourseInfo(Action):    
    def name(self) -> str:
        return "action_course_info"
    def run(self,dispatcher : CollectingDispatcher,tracker : Tracker,domain :dict):
        course_name = tracker.latest_message['entities'][0]['value']

        
        possible_course_names = [course["CourseName"] for course in db.Courses.find({},{"CourseName" : 1,"_id" : 0})]
        
        corrected_course_name = CorrectSpelling(course_name, possible_course_names)
        print(corrected_course_name)
        course = db.Courses.find_one({"CourseName": corrected_course_name})
        
        department_id = course["DepartmentId"]
        department_obj = ObjectId(department_id)
        department = db.Departments.find_one({"_id" : department_obj})
        course_type = course["CourseType"]
        course_year = course["EstablishedYear"]
        department_name = department["DepartmentName"]

        response = f"The course {course_name} is a {course_type} course offered by the {department_name} department. It was established in the year '{course_year}'."
        dispatcher.utter_message(text=response)
        return []   
    
class ActionAskCourseYear(Action):
    def name(self) -> str:
        return "action_course_year"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Retrieve course_name entity from tracker
        print(tracker.latest_message)
        course_name = tracker.latest_message['entities'][0]['value']
        print(course_name)

        possible_course_names = [course["CourseName"] for course in db.Courses.find({},{"CourseName" : 1,"_id" : 0})]
        
        corrected_course_name = CorrectSpelling(course_name, possible_course_names)
        # Query the Courses collection for the course information
        course = db.Courses.find_one({"CourseName": corrected_course_name})
        print(course)
        if course:
            # Get the established year
            established_year = course["EstablishedYear"]
            
            # Respond with the established year
            response = f"The course {course_name} was established in the year {established_year}."
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message(f"I couldn't find information for the course '{course_name}'.")

        return []      
    
class ActionAskCourseType(Action):
    def name(self) -> str:
        return "action_course_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) :
        # Retrieve course_name entity from tracker
        course_name = tracker.latest_message['entities'][0]['value']
        
        # Query the Courses collection for the course information
        

        possible_course_names = [course["CourseName"] for course in db.Courses.find({},{"CourseName" : 1,"_id" : 0})]
        
        corrected_course_name = CorrectSpelling(course_name, possible_course_names)
        course = db.Courses.find_one({"CourseName": corrected_course_name})
        if course:
            # Get the course type
            course_type = course.get("CourseType")
            
            # Respond with the course type
            response = f"The course {course_name} is a {course_type} course."
            dispatcher.utter_message(response)
        else:
            dispatcher.utter_message(f"I couldn't find information for the course '{course_name}'.")

        return []   