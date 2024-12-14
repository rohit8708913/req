#(©)CodeXBotz

import pymongo, os
from config import DB_URI, DB_NAME
import motor.motor_asyncio
from config import JOIN_REQS_DB
from pyrogram.types import ChatJoinRequest

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



# Channel 1 Database Class
class JoinReqs1:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB)
        self.db = self.client["JoinReqs_Channel1"]  # Database specific to Channel 1

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
            print(f"Error: {user_id} not added. Collection not found.")
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
            print(f"Error adding user to Channel 1: {e}")

    async def get_user(self, user_id):
        """Retrieve a user from the database."""
        col = self.get_collection()
        if not col:
            return None
        try:
            return await col.find_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error retrieving user from Channel 1: {e}")
            return None

    async def get_all_users(self):
        """Retrieve all users from the database."""
        col = self.get_collection()
        if not col:
            return []
        try:
            return await col.find().to_list(None)
        except Exception as e:
            print(f"Error retrieving all users from Channel 1: {e}")
            return []

    async def delete_user(self, user_id):
        """Delete a user from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error deleting user from Channel 1: {e}")

    async def delete_all_users(self):
        """Delete all users from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_many({})
        except Exception as e:
            print(f"Error deleting all users from Channel 1: {e}")

    async def get_all_users_count(self):
        """Get the count of all users in the database."""
        col = self.get_collection()
        if not col:
            return 0
        try:
            return await col.count_documents({})
        except Exception as e:
            print(f"Error counting users in Channel 1: {e}")
            return 0

    async def set_fsub_mode(self, mode):
        """Set the FSUB mode for the channel."""
        col = self.db["fsub_modes"]
        try:
            await col.update_one({"channel_id": 1}, {"$set": {"mode": mode}}, upsert=True)
        except Exception as e:
            print(f"Error setting FSUB mode for Channel 1: {e}")

    async def get_fsub_mode(self):
        """Get the FSUB mode for the channel."""
        col = self.db["fsub_modes"]
        try:
            doc = await col.find_one({"channel_id": 1})
            return doc["mode"] if doc else None
        except Exception as e:
            print(f"Error getting FSUB mode for Channel 1: {e}")
            return None


# Channel 2 Database Class
class JoinReqs2:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB)
        self.db = self.client["JoinReqs_Channel2"]  # Database specific to Channel 2

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
            print(f"Error: {user_id} not added. Collection not found.")
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
            print(f"Error adding user to Channel 2: {e}")

    async def get_user(self, user_id):
        """Retrieve a user from the database."""
        col = self.get_collection()
        if not col:
            return None
        try:
            return await col.find_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error retrieving user from Channel 2: {e}")
            return None

    async def get_all_users(self):
        """Retrieve all users from the database."""
        col = self.get_collection()
        if not col:
            return []
        try:
            return await col.find().to_list(None)
        except Exception as e:
            print(f"Error retrieving all users from Channel 2: {e}")
            return []

    async def delete_user(self, user_id):
        """Delete a user from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error deleting user from Channel 2: {e}")

    async def delete_all_users(self):
        """Delete all users from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_many({})
        except Exception as e:
            print(f"Error deleting all users from Channel 2: {e}")

    async def get_all_users_count(self):
        """Get the count of all users in the database."""
        col = self.get_collection()
        if not col:
            return 0
        try:
            return await col.count_documents({})
        except Exception as e:
            print(f"Error counting users in Channel 2: {e}")
            return 0

    async def set_fsub_mode(self, mode):
        """Set the FSUB mode for the channel."""
        col = self.db["fsub_modes"]
        try:
            await col.update_one({"channel_id": 2}, {"$set": {"mode": mode}}, upsert=True)
        except Exception as e:
            print(f"Error setting FSUB mode for Channel 2: {e}")

    async def get_fsub_mode(self):
        """Get the FSUB mode for the channel."""
        col = self.db["fsub_modes"]
        try:
            doc = await col.find_one({"channel_id": 2})
            return doc["mode"] if doc else None
        except Exception as e:
            print(f"Error getting FSUB mode for Channel 2: {e}")
            return None


# Channel 3 Database Class
class JoinReqs3:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB)
        self.db = self.client["JoinReqs_Channel3"]  # Database specific to Channel 3

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
            print(f"Error: {user_id} not added. Collection not found.")
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
            print(f"Error adding user to Channel 3: {e}")

    async def get_user(self, user_id):
        """Retrieve a user from the database."""
        col = self.get_collection()
        if not col:
            return None
        try:
            return await col.find_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error retrieving user from Channel 3: {e}")
            return None

    async def get_all_users(self):
        """Retrieve all users from the database."""
        col = self.get_collection()
        if not col:
            return []
        try:
            return await col.find().to_list(None)
        except Exception as e:
            print(f"Error retrieving all users from Channel 3: {e}")
            return []

    async def delete_user(self, user_id):
        """Delete a user from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error deleting user from Channel 3: {e}")

    async def delete_all_users(self):
        """Delete all users from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_many({})
        except Exception as e:
            print(f"Error deleting all users from Channel 3: {e}")

    async def get_all_users_count(self):
        """Get the count of all users in the database."""
        col = self.get_collection()
        if not col:
            return 0
        try:
            return await col.count_documents({})
        except Exception as e:
            print(f"Error counting users in Channel 3: {e}")
            return 0

    async def set_fsub_mode(self, mode):
        """Set the FSUB mode for the channel."""
        col = self.db["fsub_modes"]
        try:
            await col.update_one({"channel_id": 3}, {"$set": {"mode": mode}}, upsert=True)
        except Exception as e:
            print(f"Error setting FSUB mode for Channel 3: {e}")

    async def get_fsub_mode(self):
        """Get the FSUB mode for the channel."""
        col = self.db["fsub_modes"]
        try:
            doc = await col.find_one({"channel_id": 3})
            return doc["mode"] if doc else None
        except Exception as e:
            print(f"Error getting FSUB mode for Channel 3: {e}")
            return None


# Channel 4 Database Class
class JoinReqs4:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB)
        self.db = self.client["JoinReqs_Channel4"]  # Database specific to Channel 4

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
            print(f"Error: {user_id} not added. Collection not found.")
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
            print(f"Error adding user to Channel 4: {e}")

    async def get_user(self, user_id):
        """Retrieve a user from the database."""
        col = self.get_collection()
        if not col:
            return None
        try:
            return await col.find_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error retrieving user from Channel 4: {e}")
            return None

    async def get_all_users(self):
        """Retrieve all users from the database."""
        col = self.get_collection()
        if not col:
            return []
        try:
            return await col.find().to_list(None)
        except Exception as e:
            print(f"Error retrieving all users from Channel 4: {e}")
            return []

    async def delete_user(self, user_id):
        """Delete a user from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_one({"user_id": int(user_id)})
        except Exception as e:
            print(f"Error deleting user from Channel 4: {e}")

    async def delete_all_users(self):
        """Delete all users from the database."""
        col = self.get_collection()
        if not col:
            return
        try:
            await col.delete_many({})
        except Exception as e:
            print(f"Error deleting all users from Channel 4: {e}")

    async def get_all_users_count(self):
        """Get the count of all users in the database."""
        col = self.get_collection()
        if not col:
            return 0
        try:
            return await col.count_documents({})
        except Exception as e:
            print(f"Error counting users in Channel 4: {e}")
            return 0

    async def set_fsub_mode(self, mode):
        """Set the FSUB mode for the channel."""
        col = self.db["fsub_modes"]
        try:
            await col.update_one({"channel_id": 4}, {"$set": {"mode": mode}}, upsert=True)
        except Exception as e:
            print(f"Error setting FSUB mode for Channel 4: {e}")

    async def get_fsub_mode(self):
        """Get the FSUB mode for the channel."""
        col = self.db["fsub_modes"]
        try:
            doc = await col.find_one({"channel_id": 4})
            return doc["mode"] if doc else None
        except Exception as e:
            print(f"Error getting FSUB mode for Channel 4: {e}")
            return None