import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserNotParticipant, RPCError
from bot import Bot
from config import *
from helper_func import *
from database.database import add_user, del_user, full_userbase, present_user

FSUB_CHANNEL = None  # Default value if not set
FSUB_ENABLED = True  # Change dynamically using commands

#=====================================================================================##
WAIT_MSG = "<b>Processing ...</b>"
REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"
#=====================================================================================##

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    global FSUB_CHANNEL

    user_id = message.from_user.id
    text = message.text

    # If FSUB is disabled or FSUB_CHANNEL is not set, skip subscription check
    if not FSUB_ENABLED or not FSUB_CHANNEL:
        if not await present_user(user_id):
            try:
                await add_user(user_id)
            except:
                pass

        # If the command includes base64 encoded string, process it
        if len(text) > 7:
            try:
                base64_string = text.split(" ", 1)[1]
            except:
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
                except:
                    return  # Return early if conversion fails
            elif len(argument) == 2:
                try:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                except:
                    return

            temp_msg = await message.reply("Please wait...")
            try:
                messages = await get_messages(client, ids)
            except:
                await message.reply_text("Something went wrong..!")
                return
            await temp_msg.delete()

            track_msgs = []
            for msg in messages:
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name if msg.document else ''
                ) if bool(CUSTOM_CAPTION) and bool(msg.document) else (msg.caption.html if msg.caption else "")

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

        return

    # If FSUB is enabled, check subscription
    try:
        member = await client.get_chat_member(FSUB_CHANNEL, user_id)

        if member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
            # User is subscribed
            if not await present_user(user_id):
                try:
                    await add_user(user_id)
                except:
                    pass

            # Proceed with the command
            await start_command(client, message)
            return  # Return after handling subscription

    except UserNotParticipant:
        # If user is not a member of FSUB_CHANNEL, prompt to join
        invite_link = await client.create_chat_invite_link(FSUB_CHANNEL, creates_join_request=JOIN_REQUEST_ENABLE) if JOIN_REQUEST_ENABLE else await client.export_chat_invite_link(FSUB_CHANNEL)

        buttons = [
            [InlineKeyboardButton("Join Channel", url=invite_link)]
        ]

        try:
            buttons.append([InlineKeyboardButton("Try Again", url=f"https://t.me/{client.username}?start={message.command[1]}")])
        except IndexError:
            pass

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

@Bot.on_message(filters.command('setfsubid') & filters.user(ADMINS))
async def set_fsub_id(client: Client, message: Message):
    global FSUB_CHANNEL

    if len(message.command) != 2:
        await message.reply("Usage: /setfsubid <channel_id>")
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
        
        # If no exception occurred, update the FSUB_CHANNEL
        FSUB_CHANNEL = new_id
        await message.reply(f"Fsub channel ID has been updated to: {new_id}")

    except ValueError:
        await message.reply("Invalid channel ID. Please provide a valid number.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

@Bot.on_message(filters.command('togglefsub') & filters.user(ADMINS))
async def toggle_fsub(client: Client, message: Message):
    global FSUB_ENABLED

    # Toggle the Fsub state
    FSUB_ENABLED = not FSUB_ENABLED
    status = "enabled" if FSUB_ENABLED else "disabled"
    await message.reply(f"Fsub has been {status}.")

@Bot.on_message(filters.command('fsubstatus') & filters.user(ADMINS))
async def fsub_status(client: Client, message: Message):
    global FSUB_ENABLED
    global FSUB_CHANNEL

    status = "enabled" if FSUB_ENABLED else "disabled"
    if FSUB_ENABLED and FSUB_CHANNEL:
        channel_info = f"Channel ID: `{FSUB_CHANNEL}`"
    else:
        channel_info = "No channel set."

    await message.reply_text(
        f"**Force Subscription Status:**\n\n"
        f"**Status:** {status.capitalize()}\n"
        f"{channel_info}",
        parse_mode=ParseMode.MARKDOWN
    )
