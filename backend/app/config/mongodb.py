from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("AZURE_COSMO_DB", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("MONGO_DB_NAME", "hackathon_db")

# Create MongoDB client
client = MongoClient(MONGO_URI)
async_client = AsyncIOMotorClient(MONGO_URI)

# Get database
db = client[DATABASE_NAME]
async_db = async_client[DATABASE_NAME]

# Collections
incidents_collection = db.incidents
async_incidents_collection = async_db.incidents

alert_history_collection = db.alert_history
async_alert_history_collection = async_db.alert_history

remediation_steps_collection = db.remediation_steps
async_remediation_steps_collection = async_db.remediation_steps

# Close connection on application shutdown
def close_mongo_connection():
    client.close()
    async_client.close() 