# database/mongodb.py
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variables
mongodb_uri = os.getenv("MONGODB_URI")

# Create MongoDB client
client = MongoClient(mongodb_uri)
db = client["project"]
users_collection = db["user"]
properties_collection = db["properties"]

