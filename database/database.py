import motor.motor_asyncio
from config import DB_URI, DB_NAME
from pymongo.errors import PyMongoError

# Initialize MongoDB client
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

# Collection reference
user_data = database['users']

# Default verification status
DEFAULT_VERIFY = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

# Function to create a new user entry
def new_user(user_id: int):
    return {
        '_id': user_id,
        'verify_status': DEFAULT_VERIFY
    }

# Check if a user exists in the database
async def is_user_present(user_id: int) -> bool:
    try:
        return await user_data.find_one({'_id': user_id}) is not None
    except PyMongoError as e:
        print(f"[ERROR] Checking user existence: {e}")
        return False

# Add a new user with upsert
async def add_user(user_id: int):
    try:
        user = new_user(user_id)
        await user_data.update_one({'_id': user_id}, {'$setOnInsert': user}, upsert=True)
    except PyMongoError as e:
        print(f"[ERROR] Adding user: {e}")

# Get a user's verification status
async def get_verify_status(user_id: int):
    try:
        user = await user_data.find_one({'_id': user_id}, {'verify_status': 1})
        return user.get('verify_status', DEFAULT_VERIFY) if user else DEFAULT_VERIFY
    except PyMongoError as e:
        print(f"[ERROR] Retrieving verification status: {e}")
        return DEFAULT_VERIFY

# Update a user's verification status
async def update_verify_status(user_id: int, verify_status: dict):
    try:
        await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify_status}})
    except PyMongoError as e:
        print(f"[ERROR] Updating verification status: {e}")

# Get all user IDs in the database
async def get_all_users():
    try:
        return [doc['_id'] async for doc in user_data.find({}, {'_id': 1})]
    except PyMongoError as e:
        print(f"[ERROR] Retrieving all users: {e}")
        return []

# Delete a user from the database
async def delete_user(user_id: int):
    try:
        await user_data.delete_one({'_id': user_id})
    except PyMongoError as e:
        print(f"[ERROR] Deleting user: {e}")