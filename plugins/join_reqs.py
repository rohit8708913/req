from database.database import *
from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from config import ADMINS






# This function will handle join requests for all dynamically configured FSUB_CHANNELs
@Client.on_chat_join_request(filters.chat(lambda x: x.id in [FSUB_CHANNEL1, FSUB_CHANNEL2, FSUB_CHANNEL3, FSUB_CHANNEL4]))
async def join_reqs(client, join_req: ChatJoinRequest):

    # Determine the channel from which the user is trying to join
    if join_req.chat.id == FSUB_CHANNEL1:
        db_instance = db1  # Use db1 for Channel 1
    elif join_req.chat.id == FSUB_CHANNEL2:
        db_instance = db2  # Use db2 for Channel 2
    elif join_req.chat.id == FSUB_CHANNEL3:
        db_instance = db3  # Use db3 for Channel 3
    elif join_req.chat.id == FSUB_CHANNEL4:
        db_instance = db4  # Use db4 for Channel 4
    else:
        return  # Exit if no valid channel is specified

    # Check if the database is active and add the user
    if db_instance.is_active():
        user_id = join_req.from_user.id
        first_name = join_req.from_user.first_name
        username = join_req.from_user.username
        date = join_req.date

        # Add the user to the correct channel's database
        await db_instance.add_user(
            user_id=user_id,
            first_name=first_name,
            username=username,
            date=date
        )



@Bot.on_message(filters.command("total1") & filters.user(ADMINS))
async def total_users_channel1(client, message):
    db1 = JoinReqs1()
    total = await db1.get_all_users_count()
    await message.reply(f"Total Users in Channel 1: {total}")

@Bot.on_message(filters.command("total2") & filters.user(ADMINS))
async def total_users_channel2(client, message):
    db2 = JoinReqs2()
    total = await db2.get_all_users_count()
    await message.reply(f"Total Users in Channel 2: {total}")

@Bot.on_message(filters.command("total3") & filters.user(ADMINS))
async def total_users_channel3(client, message):
    db3 = JoinReqs3()
    total = await db3.get_all_users_count()
    await message.reply(f"Total Users in Channel 3: {total}")

@Bot.on_message(filters.command("total4") & filters.user(ADMINS))
async def total_users_channel4(client, message):
    db4 = JoinReqs4()
    total = await db4.get_all_users_count()
    await message.reply(f"Total Users in Channel 4: {total}")


@Bot.on_message(filters.command("clear1") & filters.user(ADMINS))
async def clear_users_channel1(client, message):
    db1 = JoinReqs1()
    await db1.delete_all_users()
    await message.reply("Cleared all users in Channel 1.")

@Bot.on_message(filters.command("clear2") & filters.user(ADMINS))
async def clear_users_channel2(client, message):
    db2 = JoinReqs2()
    await db2.delete_all_users()
    await message.reply("Cleared all users in Channel 2.")

@Bot.on_message(filters.command("clear3") & filters.user(ADMINS))
async def clear_users_channel2(client, message):
    db3 = JoinReqs3()
    await db3.delete_all_users()
    await message.reply("Cleared all users in Channel 3.")

@Bot.on_message(filters.command("clear4") & filters.user(ADMINS))
async def clear_users_channel4(client, message):
    db4 = JoinReqs4()
    await db4.delete_all_users()
    await message.reply("Cleared all users in Channel 4.")