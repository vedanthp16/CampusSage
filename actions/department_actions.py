from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient
from bson import ObjectId

from actions.common import CorrectSpelling

client = MongoClient("mongodb://localhost:27017/")   
db = client.CampusSage

