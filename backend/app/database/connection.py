import os
from typing import Optional

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pitchforge")

client: Optional[MongoClient] = None
db = None


def connect_db():
    global client, db

    if not MONGODB_URI:
        print("MongoDB URI not configured. Running with in-memory pitch storage.")
        return None

    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=4000)
        client.admin.command("ping")
        db = client[DATABASE_NAME]
        db.pitches.create_index("created_at")
        print("Connected to MongoDB.")
        return db
    except PyMongoError as exc:
        print(f"MongoDB unavailable. Running with in-memory pitch storage. Reason: {exc}")
        client = None
        db = None
        return None


def close_db():
    global client
    if client:
        client.close()


def get_db():
    return db
