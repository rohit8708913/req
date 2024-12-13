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
FSUB_ENABLED1 = True

FSUB_CHANNEL2 = None
FSUB_ENABLED2 = True

FSUB_CHANNEL3 = None
FSUB_ENABLED3 = True

FSUB_CHANNEL4 = None
FSUB_ENABLED4 = True

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


@Bot.on_message(filters.command('start') & subscribed1 & subscribed2 & subscribed3 & subscribed4)
async def start_command(client: Client, message: Message):
    global FSUB_CHANNEL1, FSUB_CHANNEL2, FSUB_CHANNEL3, FSUB_CHANNEL4

    user_id = message.from_user.id
    text = message.text

    # If FSUB is disabled or FSUB_CHANNEL is not set, skip subscription check
    if not FSUB_ENABLED1 or not FSUB_CHANNEL1 or not FSUB_ENABLED2 or not FSUB_CHANNEL2 or not FSUB_ENABLED3 or not FSUB_CHANNEL3 or not FSUB_ENABLED4 or not FSUB_CHANNEL4:
        pass

    # If the command includes a base64 encoded string, process it
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except IndexError:
            return  # Return early if the split fails

        string = await decode(base64_string)
        argument = string.split("-")
        ids = []

        # Handle different cases of the base64 decoded string
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except ValueError:
                return  # Return early if conversion fails
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except ValueError:
                return

        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("Something went wrong..!")
            print(f"Error fetching messages: {e}")
            return
        await temp_msg.delete()

        track_msgs = []
        for msg in messages:
            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name if msg.document else ""
                )
                if CUSTOM_CAPTION and msg.document
                else (msg.caption.html if msg.caption else "")
            )

            reply_markup = None if DISABLE_CHANNEL_BUTTON else msg.reply_markup

            if AUTO_DELETE_TIME and AUTO_DELETE_TIME > 0:
                try:
                    copied_msg_for_deletion = await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    if copied_msg_for_deletion:
                        track_msgs.append(copied_msg_for_deletion)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    copied_msg_for_deletion = await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    if copied_msg_for_deletion:
                        track_msgs.append(copied_msg_for_deletion)
                except Exception as e:
                    print(f"Error copying message: {e}")

            else:
                try:
                    await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup,
                        protect_content=PROTECT_CONTENT
                    )

        if track_msgs:
            delete_data = await client.send_message(
                chat_id=message.from_user.id,
                text=AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
            )
            # Schedule the file deletion task after all messages have been copied
            asyncio.create_task(delete_file(track_msgs, client, delete_data))
        else:
            print("No messages to track for deletion.")

        return  # Early return if we are processing a base64 string

    # Send the reply with the user's information
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("😊 About Me", callback_data="about"),
            InlineKeyboardButton("🔒 Close", callback_data="close")
        ]
    ])

    if START_PIC:
        await message.reply_photo(
            photo=START_PIC,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            quote=True
        )
    else:
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )


#=====================================================================================##
WAIT_MSG = "<b>Processing ...</b>"
REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"
#=====================================================================================##

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1

        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()
#=====================================================================================##

@Bot.on_message(filters.command('fsubstatus1') & filters.user(ADMINS))
async def fsub_status1(client: Client, message: Message):
    global FSUB_ENABLED1, FSUB_CHANNEL1

    status = "enabled" if FSUB_ENABLED1 else "disabled"
    channel_info = f"Channel ID: {FSUB_CHANNEL1 or 'Not Set'}"

    if FSUB_ENABLED1 and FSUB_CHANNEL1:
        try:
            invite_link = await client.export_chat_invite_link(FSUB_CHANNEL1)
            channel_info += f"\nInvite Link: {invite_link}"
        except Exception as e:
            channel_info += f"\nInvite Link: Error generating link ({e})"
    
    await message.reply(
        f"**Force Subscription Status for Channel 1:**\n\n"
        f"**Status:** {status.capitalize()}\n"
        f"{channel_info}"
    )

@Bot.on_message(filters.command('fsubstatus2') & filters.user(ADMINS))
async def fsub_status2(client: Client, message: Message):
    global FSUB_ENABLED2, FSUB_CHANNEL2

    status = "enabled" if FSUB_ENABLED2 else "disabled"
    channel_info = f"Channel ID: {FSUB_CHANNEL2 or 'Not Set'}"

    if FSUB_ENABLED2 and FSUB_CHANNEL2:
        try:
            invite_link = await client.export_chat_invite_link(FSUB_CHANNEL2)
            channel_info += f"\nInvite Link: {invite_link}"
        except Exception as e:
            channel_info += f"\nInvite Link: Error generating link ({e})"
    
    await message.reply(
        f"**Force Subscription Status for Channel 2:**\n\n"
        f"**Status:** {status.capitalize()}\n"
        f"{channel_info}"
    )

@Bot.on_message(filters.command('fsubstatus3') & filters.user(ADMINS))
async def fsub_status3(client: Client, message: Message):
    global FSUB_ENABLED3, FSUB_CHANNEL3

    status = "enabled" if FSUB_ENABLED3 else "disabled"
    channel_info = f"Channel ID: {FSUB_CHANNEL3 or 'Not Set'}"

    if FSUB_ENABLED3 and FSUB_CHANNEL3:
        try:
            invite_link = await client.export_chat_invite_link(FSUB_CHANNEL3)
            channel_info += f"\nInvite Link: {invite_link}"
        except Exception as e:
            channel_info += f"\nInvite Link: Error generating link ({e})"
    
    await message.reply(
        f"**Force Subscription Status for Channel 3:**\n\n"
        f"**Status:** {status.capitalize()}\n"
        f"{channel_info}"
    )

@Bot.on_message(filters.command('fsubstatus4') & filters.user(ADMINS))
async def fsub_status4(client: Client, message: Message):
    global FSUB_ENABLED4, FSUB_CHANNEL4

    status = "enabled" if FSUB_ENABLED4 else "disabled"
    channel_info = f"Channel ID: {FSUB_CHANNEL4 or 'Not Set'}"

    if FSUB_ENABLED4 and FSUB_CHANNEL4:
        try:
            invite_link = await client.export_chat_invite_link(FSUB_CHANNEL4)
            channel_info += f"\nInvite Link: {invite_link}"
        except Exception as e:
            channel_info += f"\nInvite Link: Error generating link ({e})"
    
    await message.reply(
        f"**Force Subscription Status for Channel 4:**\n\n"
        f"**Status:** {status.capitalize()}\n"
        f"{channel_info}"
    )

#=====================================================================================##