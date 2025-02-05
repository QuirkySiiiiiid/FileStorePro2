import motor.motor_asyncio
from config import DB_URI, DB_NAME
from pymongo.errors import PyMongoError

# Single persistent connection (Singleton Pattern)
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']

# Indexing _id for faster lookup
user_data.create_index([('_id', 1)], unique=True)

# Default verification status
default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

# Function to create a new user entry
def new_user(id):
    return {
        '_id': id,
        'verify_status': default_verify
    }

# Check if the user already exists
async def present_user(user_id: int):
    try:
        found = await user_data.find_one({'_id': user_id})
        return bool(found)
    except PyMongoError as e:
        print(f"Error checking user: {e}")
        return False

# Add a new user, using upsert to avoid duplicates
async def add_user(user_id: int):
    try:
        user = new_user(user_id)
        # Use upsert to add or update the user in one call
        await user_data.update_one({'_id': user_id}, {'$set': user}, upsert=True)
    except PyMongoError as e:
        print(f"Error adding user: {e}")

# Get verification status for a user
async def db_verify_status(user_id):
    try:
        user = await user_data.find_one({'_id': user_id})
        if user:
            return user.get('verify_status', default_verify)
        return default_verify
    except PyMongoError as e:
        print(f"Error retrieving verify status: {e}")
        return default_verify

# Update verification status
async def db_update_verify_status(user_id, verify):
    try:
        await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})
    except PyMongoError as e:
        print(f"Error updating verify status: {e}")

# Get all user IDs in the database
async def full_userbase():
    try:
        user_docs = user_data.find()
        user_ids = [doc['_id'] async for doc in user_docs]
        return user_ids
    except PyMongoError as e:
        print(f"Error retrieving userbase: {e}")
        return []

# Delete a user from the database
async def del_user(user_id: int):
    try:
        await user_data.delete_one({'_id': user_id})
    except PyMongoError as e:
        print(f"Error deleting user: {e}")
