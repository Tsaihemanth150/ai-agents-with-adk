from google.adk.agents import Agent
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os
from datetime import datetime, date, time
from bson import ObjectId

# Load environment variables from the .env file
load_dotenv()

# Connect to MongoDB dynamically
def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI must be set in your .env file.")
    return MongoClient(mongo_uri)

# ✅ Retrieve all collections
def get_collections():
    try:
        client = get_mongo_client()
        database_name = os.getenv("MONGO_DATABASE")
        if not database_name:
            raise ValueError("MONGO_DATABASE must be set in your .env file.")

        database = client[database_name]
        collections = database.list_collection_names()
        client.close()



        return json.dumps({"collections": collections})
    except Exception as e:
        return json.dumps({"error": str(e)})

# ✅ Retrieve all documents from a collection
def get_documents(collection_name: str) -> str:
    # 1) Block restricted collections
    restricted = ['users']
    if collection_name in restricted:
        return json.dumps({
            "error": f"Access to collection '{collection_name}' is restricted."
        })

    client = None
    try:
        client = get_mongo_client()
        db_name = os.getenv("MONGO_DATABASE")
        if not db_name:
            raise EnvironmentError("MONGO_DATABASE environment variable not set")

        db = client[db_name]
        raw_docs = list(db[collection_name].find({}, {"_id": 0}))

        # 2) Recursively strip out any datetime/date/time fields
        def strip_dates(obj):
            if isinstance(obj, dict):
                return {
                    k: strip_dates(v)
                    for k, v in obj.items()
                    # drop any value that's a date/time
                    if not isinstance(v, (datetime, date, time))
                }
            elif isinstance(obj, list):
                return [strip_dates(v) for v in obj]
            else:
                return obj

        cleaned_docs = [strip_dates(doc) for doc in raw_docs]

        # 3) JSON‑serialize, letting default=str handle ObjectId (and any other odd types)
        return json.dumps({"documents": cleaned_docs}, default=str)

    except Exception as e:
        return json.dumps({"error": str(e)})

    finally:
        if client:
            client.close()
# ✅ Insert a document into a collection

# ✅ Insert a document into a collection
def insert_document(collection_name: str, document: dict):
    try:
        client = get_mongo_client()
        database_name = os.getenv("MONGO_DATABASE")
        database = client[database_name]

        collection = database[collection_name]
        insert_result = collection.insert_one(document)
        client.close()

        return json.dumps({"message": "Document inserted successfully", "id": str(insert_result.inserted_id)})
    except Exception as e:
        return json.dumps({"error": str(e)})

# ✅ Update a document in a collection
def update_document(collection_name: str, filter_criteria: dict, update_data: dict):
    try:
        client = get_mongo_client()
        database_name = os.getenv("MONGO_DATABASE")
        database = client[database_name]

        collection = database[collection_name]
        update_result = collection.update_one(filter_criteria, {"$set": update_data})
        client.close()

        if update_result.modified_count:
            return json.dumps({"message": "Document updated successfully"})
        return json.dumps({"message": "No document matched the criteria"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# ✅ Delete a document from a collection
def delete_document(collection_name: str, filter_criteria: dict):
    try:
        client = get_mongo_client()
        database_name = os.getenv("MONGO_DATABASE")
        database = client[database_name]

        collection = database[collection_name]
        delete_result = collection.delete_one(filter_criteria)
        client.close()

        if delete_result.deleted_count:
            return json.dumps({"message": "Document deleted successfully"})
        return json.dumps({"message": "No document matched the criteria"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# ✅ MongoDB Agent Configuration
root_agent = Agent(
    name="MongoDbAgent",  # Fixed agent name (No spaces)
    model="gemini-2.0-flash-exp",  # LLM model
    tools=[get_collections, get_documents, insert_document, update_document, delete_document],  # CRUD operations
)