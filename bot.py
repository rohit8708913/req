from aiohttp import web
from plugins import web_server
from database.database import *
import pyromod.listen
from pyrogram.enums import ParseMode, ChatMemberStatus
import sys
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from helper_func import *
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

FSUB_CHANNEL1 = None
FSUB_ENABLED1 = True

FSUB_CHANNEL2 = None
FSUB_ENABLED2 = True

FSUB_CHANNEL3 = None
FSUB_ENABLED3 = True

FSUB_CHANNEL4 = None
FSUB_ENABLED4 = True

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        self.username = usr_bot_me.username  # Ensure this line is before using usr_bot_me

        try:
            await self.setup_fsub_invite_links()
            self.LOGGER(__name__).info("FSUB invite links setup complete.")
        except Exception as e:
            self.LOGGER(__name__).warning(f"Error during FSUB setup: {e}")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/rohit_1888")
        print("Welcome to Bot Modified by Rohit")

        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    async def setup_fsub_invite_links(self):
        # Helper function for invite link setup
        async def setup_channel_invite_link(channel_id, channel_enabled, db_instance, channel_name):
            if channel_enabled and channel_id:
                try:
                    mode = await db_instance.get_fsub_mode(channel_id)
                    if mode == "direct":
                        link = (await self.get_chat(channel_id)).invite_link
                        if not link:
                            await self.export_chat_invite_link(channel_id)
                            link = (await self.get_chat(channel_id)).invite_link
                        self.LOGGER(__name__).info(f"Direct invite link for {channel_name}: {link}")
                        return link
                    elif mode == "request":
                        link = (await self.create_chat_invite_link(chat_id=channel_id, creates_join_request=True)).invite_link
                        self.LOGGER(__name__).info(f"Join request invite link for {channel_name}: {link}")
                        return link
                except Exception as e:
                    self.LOGGER(__name__).warning(e)
                    self.LOGGER(__name__).warning(f"Failed to export invite link for {channel_name}!")
                    self.LOGGER(__name__).warning(f"Check {channel_name} ({channel_id}) and ensure the bot is admin with invite permissions.")
                    sys.exit()

        if FSUB_ENABLED1 and FSUB_CHANNEL1:
            self.invitelink1 = await setup_channel_invite_link(FSUB_CHANNEL1, FSUB_ENABLED1, db1, "FSUB_CHANNEL1")

        if FSUB_ENABLED2 and FSUB_CHANNEL2:
            self.invitelink2 = await setup_channel_invite_link(FSUB_CHANNEL2, FSUB_ENABLED2, db2, "FSUB_CHANNEL2")

        if FSUB_ENABLED3 and FSUB_CHANNEL3:
            self.invitelink3 = await setup_channel_invite_link(FSUB_CHANNEL3, FSUB_ENABLED3, db3, "FSUB_CHANNEL3")

        if FSUB_ENABLED4 and FSUB_CHANNEL4:
            self.invitelink4 = await setup_channel_invite_link(FSUB_CHANNEL4, FSUB_ENABLED4, db4, "FSUB_CHANNEL4")

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Ensure bot is admin in DB channel with CHANNEL_ID ({CHANNEL_ID}).")
            sys.exit()