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
FSUB_CHANNEL2 = None
FSUB_CHANNEL3 = None
FSUB_CHANNEL4 = None  # Default value if not set
FSUB_ENABLED = True  # Change dynamically using commands

    

async def is_subscribed1(filter, client, update):
    global FSUB_ENABLED, FSUB_CHANNEL1, ADMINS

    # If Fsub is disabled, allow all users
    if not FSUB_CHANNEL1 or not FSUB_ENABLED:
        return True

    user_id = update.from_user.id

    # Admins bypass the Fsub check
    if user_id in ADMINS:
        return True

    try:
        # Check if the user is a member of the FSUB_CHANNEL1
        member1 = await client.get_chat_member(chat_id=FSUB_CHANNEL1, user_id=user_id)

        # Return True if the user is a member, admin, or owner
        return member1.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]

    except UserNotParticipant:
        # Handle the case where the user is not part of the channel
        print(f"User {user_id} is not a participant of {FSUB_CHANNEL1}.")
        return False

    except RPCError as e:
        # Handle other Telegram API exceptions
        print(f"RPC error in is_subscribed filter: {e}")
        return False

    except Exception as e:
        # Catch any unexpected errors
        print(f"Error in is_subscribed filter: {e}")
        return False

# Register the filter
sub1 = filters.create(is_subscribed1)


#=====================================================================================##
async def is_subscribed2(filter, client, update):
    global FSUB_ENABLED, FSUB_CHANNEL2, ADMINS

    # If Fsub is disabled, allow all users
    if not FSUB_CHANNEL2 or not FSUB_ENABLED:
        return True

    user_id = update.from_user.id

    # Admins bypass the Fsub check
    if user_id in ADMINS:
        return True

    try:
        # Check if the user is a member of the FSUB_CHANNEL2
        member = await client.get_chat_member(chat_id=FSUB_CHANNEL2, user_id=user_id)

        # Return True if the user is a member, admin, or owner
        return member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]

    except UserNotParticipant:
        # Handle the case where the user is not part of the channel
        print(f"User {user_id} is not a participant of {FSUB_CHANNEL2}.")
        return False

    except RPCError as e:
        # Handle other Telegram API exceptions
        print(f"RPC error in is_subscribed filter: {e}")
        return False

    except Exception as e:
        # Catch any unexpected errors
        print(f"Error in is_subscribed filter: {e}")
        return False

# Register the filter
sub2 = filters.create(is_subscribed2)

#=====================================================================================##
async def is_subscribed3(filter, client, update):
    global FSUB_ENABLED, FSUB_CHANNEL3, ADMINS

    # If Fsub is disabled, allow all users
    if not FSUB_CHANNEL3 or not FSUB_ENABLED:
        return True

    user_id = update.from_user.id

    # Admins bypass the Fsub check
    if user_id in ADMINS:
        return True

    try:
        # Check if the user is a member of the FSUB_CHANNEL3
        member = await client.get_chat_member(chat_id=FSUB_CHANNEL3, user_id=user_id)

        # Return True if the user is a member, admin, or owner
        return member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]

    except UserNotParticipant:
        # Handle the case where the user is not part of the channel
        print(f"User {user_id} is not a participant of {FSUB_CHANNEL3}.")
        return False

    except RPCError as e:
        # Handle other Telegram API exceptions
        print(f"RPC error in is_subscribed filter: {e}")
        return False

    except Exception as e:
        # Catch any unexpected errors
        print(f"Error in is_subscribed filter: {e}")
        return False

# Register the filter
sub3 = filters.create(is_subscribed3)

#=====================================================================================##
async def is_subscribed4(filter, client, update):
    global FSUB_ENABLED, FSUB_CHANNEL4, ADMINS

    # If Fsub is disabled, allow all users
    if not FSUB_CHANNEL4 or not FSUB_ENABLED:
        return True

    user_id = update.from_user.id

    # Admins bypass the Fsub check
    if user_id in ADMINS:
        return True

    try:
        # Check if the user is a member of the FSUB_CHANNEL4
        member = await client.get_chat_member(chat_id=FSUB_CHANNEL4, user_id=user_id)

        # Return True if the user is a member, admin, or owner
        return member.status in [
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
        ]

    except UserNotParticipant:
        # Handle the case where the user is not part of the channel
        print(f"User {user_id} is not a participant of {FSUB_CHANNEL4}.")
        return False

    except RPCError as e:
        # Handle other Telegram API exceptions
        print(f"RPC error in is_subscribed filter: {e}")
        return False

    except Exception as e:
        # Catch any unexpected errors
        print(f"Error in is_subscribed filter: {e}")
        return False

# Register the filter
sub4 = filters.create(is_subscribed4)
#=====================================================================================##
WAIT_MSG = "<b>Processing ...</b>"
REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"
#=====================================================================================##

@Bot.on_message(filters.command('start') & sub1 & sub2 & sub3 & sub4)
async def start_command(client: Client, message: Message):
    global FSUB_CHANNEL1, FSUB_CHANNEL2, FSUB_CHANNEL3, FSUB_CHANNEL4

    user_id = message.from_user.id
    text = message.text

    # If FSUB is disabled or FSUB_CHANNEL is not set, skip subscription check
    if not FSUB_ENABLED or not FSUB_CHANNEL1 or not FSUB_CHANNEL2 or not FSUB_CHANNEL3 or not FSUB_CHANNEL4:
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
 
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    global FSUB_CHANNEL1, FSUB_CHANNEL2, FSUB_CHANNEL3, FSUB_CHANNEL4

    # Use the is_subscribed filter for checking membership
    user_id = message.from_user.id

    try:
        # Check if the user is subscribed to FSUB_CHANNEL1
        sub1 = await is_subscribed1(None, client, message)
        # Check if the user is subscribed to FSUB_CHANNEL2
        sub2 = await is_subscribed2(None, client, message)
        # Check if the user is subscribed to FSUB_CHANNEL3
        sub3 = await is_subscribed3(None, client, message)
        # Check if the user is subscribed to FSUB_CHANNEL4
        sub4 = await is_subscribed4(None, client, message)

        # If the user is subscribed to any channel
        if sub1 or sub2 or sub3 or sub4:
            if not await present_user(user_id):
                try:
                    await add_user(user_id)
                except Exception as e:
                    print(f"Error adding user: {e}")
            await start_command(client, message)
            return  # User is subscribed to at least one channel, so we return

        # If the user is not subscribed to any channel, prepare the join buttons
        buttons = []

        # Handle all the possible subscription combinations
        if not sub1 and not sub2 and not sub3 and not sub4:
            # User is not subscribed to any channel
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink1),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink2),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink3),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink4),
                ]
            )
        elif sub1 and not sub2 and not sub3 and not sub4:
            # User is subscribed to Channel 1 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink2),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink3),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink4),
                ]
            )
        elif sub2 and not sub1 and not sub3 and not sub4:
            # User is subscribed to Channel 2 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink1),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink3),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink4),
                ]
            )
        elif sub3 and not sub1 and not sub2 and not sub4:
            # User is subscribed to Channel 3 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink1),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink2),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink4),
                ]
            )
        elif sub4 and not sub1 and not sub2 and not sub3:
            # User is subscribed to Channel 4 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink1),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink2),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink3),
                ]
            )
        elif sub1 and sub2 and not sub3 and not sub4:
            # User is subscribed to Channel 1 and 2 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink3),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink4),
                ]
            )
        elif sub1 and not sub2 and sub3 and not sub4:
            # User is subscribed to Channel 1 and 3 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink2),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink4),
                ]
            )
        elif sub1 and not sub2 and not sub3 and sub4:
            # User is subscribed to Channel 1 and 4 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink2),
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink3),
                ]
            )
        elif not sub1 and sub2 and sub3 and not sub4:
            # User is subscribed to Channel 2 and 3 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink4),
                ]
            )
        elif not sub1 and sub2 and not sub3 and sub4:
            # User is subscribed to Channel 2 and 4 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink3),
                ]
            )
        elif not sub1 and not sub2 and sub3 and sub4:
            # User is subscribed to Channel 3 and 4 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink1),
                ]
            )
        elif sub1 and sub2 and sub3 and not sub4:
            # User is subscribed to Channel 1, 2, and 3 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink4),
                ]
            )
        elif sub1 and sub2 and not sub3 and sub4:
            # User is subscribed to Channel 1, 2, and 4 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink3),
                ]
            )
        elif sub1 and not sub2 and sub3 and sub4:
            # User is subscribed to Channel 1, 3, and 4 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink2),
                ]
            )
        elif not sub1 and sub2 and sub3 and sub4:
            # User is subscribed to Channel 2, 3, and 4 only
            buttons.append(
                [
                    InlineKeyboardButton(text="• ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ •", url=client.invitelink1),
                ]
            )
        elif sub1 and sub2 and sub3 and sub4:
            # User is subscribed to all channels
            await start_command(client, message)
            return  # No buttons are needed, user is already subscribed to all channels

        # Add a "Try Again" button as before
        try:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text='• ᴛʀʏ ᴀɢᴀɪɴ •',
                        url=f"https://t.me/{client.username}?start={message.command[1]}"
                    )
                ]
            )
        except IndexError:
            pass

        # Send the reply with the join buttons
        await message.reply(
            FORCE_MSG.format(
                first=message.from_user.first_name or "User",
                last=message.from_user.last_name or "",
                username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except Exception as e:
        print(f"Error while checking membership: {e}")

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

#=====================================================================================##

@Bot.on_message(filters.command('fsubstatus') & filters.user(ADMINS))
async def fsub_status(client: Client, message: Message):
    global FSUB_ENABLED
    global FSUB_CHANNEL1, FSUB_CHANNEL2, FSUB_CHANNEL3, FSUB_CHANNEL4

    status = "enabled" if FSUB_ENABLED else "disabled"

    # Check the status for each channel
    channel_1_info = f"Channel 1 ID: `{FSUB_CHANNEL1}`" if FSUB_CHANNEL1 else "Channel 1: No channel set."
    channel_2_info = f"Channel 2 ID: `{FSUB_CHANNEL2}`" if FSUB_CHANNEL2 else "Channel 2: No channel set."
    channel_3_info = f"Channel 3 ID: `{FSUB_CHANNEL3}`" if FSUB_CHANNEL3 else "Channel 3: No channel set."
    channel_4_info = f"Channel 4 ID: `{FSUB_CHANNEL4}`" if FSUB_CHANNEL4 else "Channel 4: No channel set."

    # Send the reply
    await message.reply_text(
        f"**Force Subscription Status:**\n\n"
        f"**Status:** {status.capitalize()}\n\n"
        f"{channel_1_info}\n"
        f"{channel_2_info}\n"
        f"{channel_3_info}\n"
        f"{channel_4_info}",
        parse_mode=ParseMode.MARKDOWN
    )

#=====================================================================================##

@Bot.on_message(filters.command('togglefsub') & filters.user(ADMINS))
async def toggle_fsub(client: Client, message: Message):
    global FSUB_ENABLED, FSUB_CHANNEL1, FSUB_CHANNEL2, FSUB_CHANNEL3, FSUB_CHANNEL4

    # Toggle the global Fsub state
    FSUB_ENABLED = not FSUB_ENABLED
    status = "enabled" if FSUB_ENABLED else "disabled"

    if not FSUB_ENABLED:
        # If globally disabled, turn off all individual channels
        FSUB_CHANNEL1 = None
        FSUB_CHANNEL2 = None
        FSUB_CHANNEL3 = None
        FSUB_CHANNEL4 = None
        await message.reply(
            f"Fsub has been globally {status}. All channels have been disabled."
        )
    else:
        await message.reply(f"Fsub has been globally {status}.")


@Bot.on_message(filters.command('togglefsub1') & filters.user(ADMINS))
async def toggle_fsub1(client: Client, message: Message):
    global FSUB_CHANNEL1

    if FSUB_CHANNEL1:
        FSUB_CHANNEL1 = None
        status = "enabled"
    else:
        FSUB_CHANNEL1 = None  # Replace with the actual channel ID dynamically if needed
        status = "disabled"

    await message.reply(f"Fsub for Channel 1 has been {status}.")


@Bot.on_message(filters.command('togglefsub2') & filters.user(ADMINS))
async def toggle_fsub2(client: Client, message: Message):
    global FSUB_CHANNEL2

    if FSUB_CHANNEL2:
        FSUB_CHANNEL2 = None
        status = "enabled"
    else:
        FSUB_CHANNEL2 = None  # Replace with the actual channel ID dynamically if needed
        status = "disabled"

    await message.reply(f"Fsub for Channel 2 has been {status}.")


@Bot.on_message(filters.command('togglefsub3') & filters.user(ADMINS))
async def toggle_fsub3(client: Client, message: Message):
    global FSUB_CHANNEL3

    if FSUB_CHANNEL3:
        FSUB_CHANNEL3 = None
        status = "enabled"
    else:
        FSUB_CHANNEL3 = None  # Replace with the actual channel ID dynamically if needed
        status = "disabled"

    await message.reply(f"Fsub for Channel 3 has been {status}.")


@Bot.on_message(filters.command('togglefsub4') & filters.user(ADMINS))
async def toggle_fsub4(client: Client, message: Message):
    global FSUB_CHANNEL4

    if FSUB_CHANNEL4:
        FSUB_CHANNEL4 = None
        status = "enabled"
    else:
        FSUB_CHANNEL4 = None  # Replace with the actual channel ID dynamically if needed
        status = "disabled"

    await message.reply(f"Fsub for Channel 4 has been {status}.")

#=====================================================================================##

@Bot.on_message(filters.command('setfsubid1') & filters.user(ADMINS))
async def set_fsub_id1(client: Client, message: Message):
    global FSUB_CHANNEL1

    if len(message.command) != 2:
        await message.reply("Usage: /setfsubid1 <channel_id>")
        return

    try:
        new_id = int(message.command[1])

        # Get bot's user information
        bot_info = await client.get_me()

        # Check if the bot is an admin in the specified channel
        bot_member = await client.get_chat_member(new_id, bot_info.id)
        if bot_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await message.reply("The bot is not an admin of this channel. Please make the bot an admin and try again.")
            return

        # Try to get the invite link from the channel to ensure the bot can access it
        try:
            invite_link = await client.export_chat_invite_link(new_id)
        except Exception as e:
            await message.reply(f"Error: The bot doesn't have permission to get the invite link for this channel. Error: {str(e)}")
            return

        # If no exception occurred, update the FSUB_CHANNEL1
        FSUB_CHANNEL1 = new_id
        await message.reply(f"Fsub channel 1 ID has been updated to: {new_id}")

    except ValueError:
        await message.reply("Invalid channel ID. Please provide a valid number.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@Bot.on_message(filters.command('setfsubid2') & filters.user(ADMINS))
async def set_fsub_id2(client: Client, message: Message):
    global FSUB_CHANNEL2

    if len(message.command) != 2:
        await message.reply("Usage: /setfsubid2 <channel_id>")
        return

    try:
        new_id = int(message.command[1])

        # Get bot's user information
        bot_info = await client.get_me()

        # Check if the bot is an admin in the specified channel
        bot_member = await client.get_chat_member(new_id, bot_info.id)
        if bot_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await message.reply("The bot is not an admin of this channel. Please make the bot an admin and try again.")
            return

        # Try to get the invite link from the channel to ensure the bot can access it
        try:
            invite_link = await client.export_chat_invite_link(new_id)
        except Exception as e:
            await message.reply(f"Error: The bot doesn't have permission to get the invite link for this channel. Error: {str(e)}")
            return

        # If no exception occurred, update the FSUB_CHANNEL2
        FSUB_CHANNEL2 = new_id
        await message.reply(f"Fsub channel 2 ID has been updated to: {new_id}")

    except ValueError:
        await message.reply("Invalid channel ID. Please provide a valid number.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@Bot.on_message(filters.command('setfsubid3') & filters.user(ADMINS))
async def set_fsub_id3(client: Client, message: Message):
    global FSUB_CHANNEL3

    if len(message.command) != 2:
        await message.reply("Usage: /setfsubid3 <channel_id>")
        return

    try:
        new_id = int(message.command[1])

        # Get bot's user information
        bot_info = await client.get_me()

        # Check if the bot is an admin in the specified channel
        bot_member = await client.get_chat_member(new_id, bot_info.id)
        if bot_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await message.reply("The bot is not an admin of this channel. Please make the bot an admin and try again.")
            return

        # Try to get the invite link from the channel to ensure the bot can access it
        try:
            invite_link = await client.export_chat_invite_link(new_id)
        except Exception as e:
            await message.reply(f"Error: The bot doesn't have permission to get the invite link for this channel. Error: {str(e)}")
            return

        # If no exception occurred, update the FSUB_CHANNEL3
        FSUB_CHANNEL3 = new_id
        await message.reply(f"Fsub channel 3 ID has been updated to: {new_id}")

    except ValueError:
        await message.reply("Invalid channel ID. Please provide a valid number.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@Bot.on_message(filters.command('setfsubid4') & filters.user(ADMINS))
async def set_fsub_id4(client: Client, message: Message):
    global FSUB_CHANNEL4

    if len(message.command) != 2:
        await message.reply("Usage: /setfsubid4 <channel_id>")
        return

    try:
        new_id = int(message.command[1])

        # Get bot's user information
        bot_info = await client.get_me()

        # Check if the bot is an admin in the specified channel
        bot_member = await client.get_chat_member(new_id, bot_info.id)
        if bot_member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            await message.reply("The bot is not an admin of this channel. Please make the bot an admin and try again.")
            return

        # Try to get the invite link from the channel to ensure the bot can access it
        try:
            invite_link = await client.export_chat_invite_link(new_id)
        except Exception as e:
            await message.reply(f"Error: The bot doesn't have permission to get the invite link for this channel. Error: {str(e)}")
            return

        # If no exception occurred, update the FSUB_CHANNEL4
        FSUB_CHANNEL4 = new_id
        await message.reply(f"Fsub channel 4 ID has been updated to: {new_id}")

    except ValueError:
        await message.reply("Invalid channel ID. Please provide a valid number.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

#=====================================================================================##


