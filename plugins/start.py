import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.errors import ChatIdInvalid, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserNotParticipant, RPCError
from bot import Bot
from config import *
from helper_func import *
from database.database import add_user, del_user, full_userbase, present_user

#=====================================================================================##
FSUB_CHANNEL1 = None
FSUB_ENABLED1 = False

FSUB_CHANNEL2 = None
FSUB_ENABLED2 = False

FSUB_CHANNEL3 = None
FSUB_ENABLED3 = False

FSUB_CHANNEL4 = None
FSUB_ENABLED4 = False

async def is_subscribed1(_, client: Client, update: Message):
    if not FSUB_ENABLED1 or not FSUB_CHANNEL1:
        return True

    try:
        member = await client.get_chat_member(chat_id=FSUB_CHANNEL1, user_id=update.from_user.id)
        return member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking subscription for Channel 1: {e}")
        return False


subscribed1 = filters.create(is_subscribed1)

#=====================================================================================##

async def is_subscribed2(_, client: Client, update: Message):
    if not FSUB_ENABLED2 or not FSUB_CHANNEL2:
        return True

    try:
        member = await client.get_chat_member(chat_id=FSUB_CHANNEL2, user_id=update.from_user.id)
        return member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking subscription for Channel 2: {e}")
        return False


subscribed2 = filters.create(is_subscribed2)

#=====================================================================================##

async def is_subscribed3(_, client: Client, update: Message):
    if not FSUB_ENABLED3 or not FSUB_CHANNEL3:
        return True

    try:
        member = await client.get_chat_member(chat_id=FSUB_CHANNEL3, user_id=update.from_user.id)
        return member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking subscription for Channel 3: {e}")
        return False


subscribed3 = filters.create(is_subscribed3)

#=====================================================================================##

async def is_subscribed4(_, client: Client, update: Message):
    if not FSUB_ENABLED4 or not FSUB_CHANNEL4:
        return True

    try:
        member = await client.get_chat_member(chat_id=FSUB_CHANNEL4, user_id=update.from_user.id)
        return member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]
    except UserNotParticipant:
        return False
    except Exception as e:
        print(f"Error checking subscription for Channel 4: {e}")
        return False


subscribed4 = filters.create(is_subscribed4)

#=====================================================================================##
@Bot.on_message(filters.command('setfsub1') & filters.user(ADMINS))
async def set_fsub1(client: Client, message: Message):
    global FSUB_CHANNEL1
    if len(message.command) != 2:
        await message.reply("Usage: /setfsub1 <channel_id>")
        return

    try:
        channel_id = int(message.command[1])
        bot_info = await client.get_me()
        bot_member = await client.get_chat_member(chat_id=channel_id, user_id=bot_info.id)
        if bot_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await message.reply("The bot must be an admin in the channel.")
            return

        FSUB_CHANNEL1 = channel_id
        await message.reply(f"Channel 1 FSUB set to ID: {channel_id}")
    except Exception as e:
        await message.reply(f"Error: {e}")

@Bot.on_message(filters.command('setfsub2') & filters.user(ADMINS))
async def set_fsub2(client: Client, message: Message):
    global FSUB_CHANNEL2
    if len(message.command) != 2:
        await message.reply("Usage: /setfsub2 <channel_id>")
        return

    try:
        channel_id = int(message.command[1])
        bot_info = await client.get_me()
        bot_member = await client.get_chat_member(chat_id=channel_id, user_id=bot_info.id)
        if bot_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await message.reply("The bot must be an admin in the channel.")
            return

        FSUB_CHANNEL1 = channel_id
        await message.reply(f"Channel 2 FSUB set to ID: {channel_id}")
    except Exception as e:
        await message.reply(f"Error: {e}")

@Bot.on_message(filters.command('setfsub3') & filters.user(ADMINS))
async def set_fsub3(client: Client, message: Message):
    global FSUB_CHANNEL3
    if len(message.command) != 2:
        await message.reply("Usage: /setfsub3 <channel_id>")
        return

    try:
        channel_id = int(message.command[1])
        bot_info = await client.get_me()
        bot_member = await client.get_chat_member(chat_id=channel_id, user_id=bot_info.id)
        if bot_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await message.reply("The bot must be an admin in the channel.")
            return

        FSUB_CHANNEL3 = channel_id
        await message.reply(f"Channel 3 FSUB set to ID: {channel_id}")
    except Exception as e:
        await message.reply(f"Error: {e}")

@Bot.on_message(filters.command('setfsub4') & filters.user(ADMINS))
async def set_fsub4(client: Client, message: Message):
    global FSUB_CHANNEL4
    if len(message.command) != 2:
        await message.reply("Usage: /setfsub4 <channel_id>")
        return

    try:
        channel_id = int(message.command[1])
        bot_info = await client.get_me()
        bot_member = await client.get_chat_member(chat_id=channel_id, user_id=bot_info.id)
        if bot_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await message.reply("The bot must be an admin in the channel.")
            return

        FSUB_CHANNEL4 = channel_id
        await message.reply(f"Channel 4 FSUB set to ID: {channel_id}")
    except Exception as e:
        await message.reply(f"Error: {e}")
#=====================================================================================##

@Bot.on_message(filters.command('togglefsub1') & filters.user(ADMINS))
async def toggle_fsub1(client: Client, message: Message):
    global FSUB_ENABLED1
    FSUB_ENABLED1 = not FSUB_ENABLED1
    status = "enabled" if FSUB_ENABLED1 else "disabled"
    await message.reply(f"FSUB for Channel 1 is now {status}.")

@Bot.on_message(filters.command('togglefsub2') & filters.user(ADMINS))
async def toggle_fsub2(client: Client, message: Message):
    global FSUB_ENABLED2
    FSUB_ENABLED2 = not FSUB_ENABLED2
    status = "enabled" if FSUB_ENABLED2 else "disabled"
    await message.reply(f"FSUB for Channel 2 is now {status}.")

@Bot.on_message(filters.command('togglefsub3') & filters.user(ADMINS))
async def toggle_fsub3(client: Client, message: Message):
    global FSUB_ENABLED3
    FSUB_ENABLED3 = not FSUB_ENABLED3
    status = "enabled" if FSUB_ENABLED3 else "disabled"
    await message.reply(f"FSUB for Channel 3 is now {status}.")

@Bot.on_message(filters.command('togglefsub4') & filters.user(ADMINS))
async def toggle_fsub4(client: Client, message: Message):
    global FSUB_ENABLED4
    FSUB_ENABLED4 = not FSUB_ENABLED4
    status = "enabled" if FSUB_ENABLED4 else "disabled"
    await message.reply(f"FSUB for Channel 4 is now {status}.")

#=====================================================================================##

