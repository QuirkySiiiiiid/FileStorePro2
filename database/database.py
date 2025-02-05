import motor.motor_asyncio
from config import DB_URI, DB_NAME
from pymongo.errors import PyMongoError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize MongoDB client
try:
    dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
    database = dbclient[DB_NAME]
    # Test connection
    dbclient.admin.command("ping")
    logging.info("✅ Successfully connected to MongoDB.")
except PyMongoError as e:
    logging.error(f"❌ Failed to connect to MongoDB: {e}")
    raise SystemExit("Database connection failed. Exiting...")

# Collection reference
user_data = database['users']

# Default verification status
DEFAULT_VERIFY = {
    "is_verified": False,
    "verified_time": 0,
    "verify_token": "",
    "link": ""
}

def new_user(user_id: int) -> dict:
    """
    Create a new user entry.
    """
    return {
        "_id": user_id,
        "verify_status": DEFAULT_VERIFY
    }

async def is_user_present(user_id: int) -> bool:
    """
    Check if a user exists in the database.
    """
    try:
        return await user_data.find_one({"_id": user_id}, {"_id": 1}) is not None
    except PyMongoError as e:
        logging.error(f"[ERROR] Checking user existence: {e}")
        return False

async def add_user(user_id: int):
    """
    Add a new user to the database using upsert.
    """
    try:
        user = new_user(user_id)
        await user_data.update_one({"_id": user_id}, {"$setOnInsert": user}, upsert=True)
        logging.info(f"✅ User {user_id} added (or already exists).")
    except PyMongoError as e:
        logging.error(f"[ERROR] Adding user {user_id}: {e}")

async def get_verify_status(user_id: int) -> dict:
    """
    Retrieve a user's verification status.
    """
    try:
        user = await user_data.find_one({"_id": user_id}, {"verify_status": 1})
        return user.get("verify_status", DEFAULT_VERIFY) if user else DEFAULT_VERIFY
    except PyMongoError as e:
        logging.error(f"[ERROR] Retrieving verification status for {user_id}: {e}")
        return DEFAULT_VERIFY

async def update_verify_status(user_id: int, verify_status: dict):
    """
    Update a user's verification status.
    """
    try:
        await user_data.update_one({"_id": user_id}, {"$set": {"verify_status": verify_status}})
        logging.info(f"✅ Updated verification status for user {user_id}.")
    except PyMongoError as e:
        logging.error(f"[ERROR] Updating verification status for {user_id}: {e}")

async def get_all_users() -> list:
    """
    Retrieve all user IDs in the database.
    """
    try:
        return [doc["_id"] async for doc in user_data.find({}, {"_id": 1})]
    except PyMongoError as e:
        logging.error(f"[ERROR] Retrieving all users: {e}")
        return []

async def delete_user(user_id: int):
    """
    Delete a user from the database.
    """
    try:
        await user_data.delete_one({"_id": user_id})
        logging.info(f"✅ User {user_id} deleted.")
    except PyMongoError as e:
        logging.error(f"[ERROR] Deleting user {user_id}: {e}")