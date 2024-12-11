from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from config import (
    API_HASH,
    APP_ID,
    LOGGER,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
    CHANNEL_ID,
    PORT,
    ADMINS,
)

# Dynamic Fsub variables
FSUB_ENABLED = True  # Force subscription enabled by default
FSUB_CHANNEL = None  # Dynamic channel ID (set via commands)

ascii_art = """
██████╗░░█████╗░██╗░░██╗██╗████████╗
██╔══██╗██╔══██╗██║░██╔╝██║╚══██╔══╝
██████╦╝██║░░██║█████═╝░██║░░░██║░░░
██╔══██╗██║░░██║██╔═██╗░██║░░░██║░░░
██████╦╝╚█████╔╝██║░╚██╗██║░░░██║░░░
╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        global FSUB_CHANNEL

        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Force subscription dynamic setup
        if FSUB_ENABLED and FSUB_CHANNEL:
            try:
                link = (await self.get_chat(FSUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_CHANNEL)
                    link = (await self.get_chat(FSUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning("Failed to export invite link for Fsub channel!")
                self.LOGGER(__name__).warning(f"Check FSUB_CHANNEL ({FSUB_CHANNEL}) and ensure the bot is admin with invite permissions.")
                sys.exit()

        # Validate DB channel access
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Ensure bot is admin in DB channel with CHANNEL_ID ({CHANNEL_ID}).")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/CodeXBotz")
        print(ascii_art)
        print("Welcome to CodeXBotz File Sharing Bot")
        self.username = usr_bot_me.username

        # Web server setup
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")


# Commands for dynamically managing Fsub
@Bot.on_message(filters.command("togglefsub") & filters.user(ADMINS))
async def toggle_fsub(client: Client, message: Message):
    global FSUB_ENABLED
    FSUB_ENABLED = not FSUB_ENABLED
    status = "enabled" if FSUB_ENABLED else "disabled"
    await message.reply(f"Force subscription has been {status}.")


@Bot.on_message(filters.command("setfsubid") & filters.user(ADMINS))
async def set_fsub_id(client: Client, message: Message):
    global FSUB_CHANNEL

    if len(message.command) != 2:
        await message.reply("Usage: /setfsubid <channel_id>")
        return

    try:
        FSUB_CHANNEL = int(message.command[1])
        await message.reply(f"Fsub channel ID updated to: {FSUB_CHANNEL}")
    except ValueError:
        await message.reply("Invalid channel ID. Please provide a valid number.")