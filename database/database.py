#(©)CodeXBotz

import pymongo, os
from config import DB_URI, DB_NAME
import motor.motor_asyncio
from config import JOIN_REQS_DB

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
        
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return




class JoinReqsBase:
    """Base class for all channel join request databases."""
    def __init__(self, db_name: str):
        """Initialize the database connection for a specific channel."""
        if JOIN_REQS_DB:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB)
            self.db = self.client[db_name]  # Database specific to this channel
        else:
            self.client = None
            self.db = None

    def is_active(self):
        """Check if the database connection is active."""
        return self.client is not None

    def get_collection(self):
        """Get the collection for this specific channel."""
        if not self.is_active():
            return None
        return self.db["users"]

    async def add_user(self, user_id, first_name, username, date):
        """Add a user to the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.insert_one({
                "_id": int(user_id),
                "user_id": int(user_id),
                "first_name": first_name,
                "username": username,
                "date": date,
            })
        except Exception as e:
            print(f"Error adding user to the channel: {e}")

    async def get_user(self, user_id):
        """Retrieve a user from the database."""
        col = self.get_collection()
        if not col:
            return None
        try:
            return await col.find_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error retrieving user from the channel: {e}")
            return None

    async def get_all_users(self):
        """Retrieve all users from the database."""
        col = self.get_collection()
        if not col:
            return []
        try:
            return await col.find().to_list(None)
        except Exception as e:
            print(f"Error retrieving all users from the channel: {e}")
            return []

    async def delete_user(self, user_id):
        """Delete a user from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error deleting user from the channel: {e}")

    async def delete_all_users(self):
        """Delete all users from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_many({})
        except Exception as e:
            print(f"Error deleting all users from the channel: {e}")

    async def get_all_users_count(self):
        """Get the count of all users in the database."""
        col = self.get_collection()
        if not col:
            return 0
        try:
            return await col.count_documents({})
        except Exception as e:
            print(f"Error counting users in the channel: {e}")
            return 0


# Now we create separate classes for each channel, inheriting from JoinReqsBase

class JoinReqs1(JoinReqsBase):
    def __init__(self):
        super().__init__("JoinReqs_Channel1")  # Use the specific database for Channel 1


class JoinReqs2(JoinReqsBase):
    def __init__(self):
        super().__init__("JoinReqs_Channel2")  # Use the specific database for Channel 2


class JoinReqs3(JoinReqsBase):
    def __init__(self):
        super().__init__("JoinReqs_Channel3")  # Use the specific database for Channel 3


class JoinReqs4(JoinReqsBase):
    def __init__(self):
        super().__init__("JoinReqs_Channel4")  # Use the specific database for Channel 4