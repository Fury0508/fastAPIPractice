from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["mydb"]

contracts_collection = db['contracts']
analysis_collection = db['analysis']


def init_db():
    # Create indexes for the collections if needed
    contracts_collection.create_index("contract_id", unique=True)
    analysis_collection.create_index("analysis_id", unique=True)
    