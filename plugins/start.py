import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from config import FORCE_MSG, START_MSG, FSUB_CHANNEL, JOIN_REQUEST_ENABLE, FORCE_SUB_CHANNEL
from helper_func import get_messages, decode, delete_file
from bot import Bot

# Define initial FSUB status (enabled by default)
FSUB_ENABLED = True  # Change dynamically using commands


# Check if the user is subscribed to the FSUB_CHANNEL
async def is_user_subscribed(client: Client, user_id: int) -> bool:
    try:
        # Check if the user is a member of the FSUB_CHANNEL
        user = await client.get_chat_member(FSUB_CHANNEL, user_id)
        if user.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Error checking subscription: {e}")
    return False


@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    global FSUB_ENABLED

    # If FSUB is disabled, proceed with the welcome message
    if not FSUB_ENABLED or not FSUB_CHANNEL:
        await message.reply(
            START_MSG.format(
                first=message.from_user.first_name or "User",
                last=message.from_user.last_name or "",
                username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                mention=message.from_user.mention,
                id=message.from_user.id,
            )
        )
        return

    # If FSUB is enabled, check subscription
    user_id = message.from_user.id
    is_subscribed = await is_user_subscribed(client, user_id)

    if is_subscribed:
        # Proceed with normal behavior if the user is subscribed
        text = message.text
        if len(text) > 7:
            try:
                base64_string = text.split(" ", 1)[1]
            except:
                return
            string = await decode(base64_string)
            argument = string.split("-")
            if len(argument) == 3:
                try:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))
                except:
                    return
                if start <= end:
                    ids = range(start, end + 1)
                else:
                    ids = []
                    i = start
                    while True:
                        ids.append(i)
                        i -= 1
                        if i < end:
                            break
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
                caption = msg.caption.html if msg.caption else ""

                if AUTO_DELETE_TIME and AUTO_DELETE_TIME > 0:
                    try:
                        copied_msg_for_deletion = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML)
                        if copied_msg_for_deletion:
                            track_msgs.append(copied_msg_for_deletion)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        copied_msg_for_deletion = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML)
                        if copied_msg_for_deletion:
                            track_msgs.append(copied_msg_for_deletion)

                else:
                    try:
                        await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML)

            if track_msgs:
                delete_data = await client.send_message(
                    chat_id=message.from_user.id,
                    text="Your files will be deleted in {AUTO_DELETE_TIME} seconds"
                )
                # Schedule the file deletion task after all messages have been copied
                asyncio.create_task(delete_file(track_msgs, client, delete_data))
            else:
                print("No messages to track for deletion.")

            return
        else:
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("😊 About Me", callback_data="about"),
                        InlineKeyboardButton("🔒 Close", callback_data="close")
                    ]
                ]
            )
            if START_PIC:  # Check if START_PIC has a value
                await message.reply_photo(
                    photo=START_PIC,
                    caption=START_MSG.format(
                        first=message.from_user.first_name,
                        last=message.from_user.last_name,
                        username=None if not message.from_user.username else '@' + message.from_user.username,
                        mention=message.from_user.mention,
                        id=message.from_user.id
                    ),
                    reply_markup=reply_markup,
                    quote=True
                )
            else:  # If START_PIC is empty, send only the text
                await message.reply_text(
                    text=START_MSG.format(
                        first=message.from_user.first_name,
                        last=message.from_user.last_name,
                        username=None if not message.from_user.username else '@' + message.from_user.username,
                        mention=message.from_user.mention,
                        id=message.from_user.id
                    ),
                    reply_markup=reply_markup,
                    disable_web_page_preview=True,
                    quote=True
                )
            return
    else:
        # If the user is not subscribed, send Force Subscription message
        invite_link = (
            await client.create_chat_invite_link(
                chat_id=FSUB_CHANNEL, creates_join_request=JOIN_REQUEST_ENABLE
            )
            if JOIN_REQUEST_ENABLE
            else await client.export_chat_invite_link(FSUB_CHANNEL)
        )
        buttons = [
            [
                InlineKeyboardButton(
                    "Join Channel",
                    url=invite_link
                )
            ]
        ]

        try:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text='Try Again',
                        url=f"https://t.me/{client.username}?start={message.command[1]}"
                    )
                ]
            )
        except IndexError:
            pass

        await message.reply(
            FORCE_MSG.format(
                first=message.from_user.first_name or "User",
                last=message.from_user.last_name or "",
                username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                mention=message.from_user.mention,
                id=message.from_user.id,
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )