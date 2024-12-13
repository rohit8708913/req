from aiohttp import web
from plugins import web_server

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

# Dynamic Fsub variables for 4 channels
FSUB_ENABLED = True  # Force subscription enabled by default
FSUB_CHANNEL1 = None  # Dynamic channel ID (set via commands)
FSUB_CHANNEL2 = None
FSUB_CHANNEL3 = None
FSUB_CHANNEL4 = None


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
        global FSUB_CHANNEL1, FSUB_CHANNEL2, FSUB_CHANNEL3, FSUB_CHANNEL4

        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Force subscription dynamic setup for all channels separately
        if FSUB_ENABLED1 and FSUB_CHANNEL1:
            try:
                link = (await self.get_chat(FSUB_CHANNEL1)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_CHANNEL1)
                    link = (await self.get_chat(FSUB_CHANNEL1)).invite_link
                self.invitelink1 = link
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning("Failed to export invite link for Fsub channel 1!")
                self.LOGGER(__name__).warning(f"Check FSUB_CHANNEL1 ({FSUB_CHANNEL1}) and ensure the bot is admin with invite permissions.")
                sys.exit()

        if FSUB_ENABLED2 and FSUB_CHANNEL2:
            try:
                link = (await self.get_chat(FSUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_CHANNEL2)
                    link = (await self.get_chat(FSUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning("Failed to export invite link for Fsub channel 2!")
                self.LOGGER(__name__).warning(f"Check FSUB_CHANNEL2 ({FSUB_CHANNEL2}) and ensure the bot is admin with invite permissions.")
                sys.exit()

        if FSUB_ENABLED3 and FSUB_CHANNEL3:
            try:
                link = (await self.get_chat(FSUB_CHANNEL3)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_CHANNEL3)
                    link = (await self.get_chat(FSUB_CHANNEL3)).invite_link
                self.invitelink3 = link
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning("Failed to export invite link for Fsub channel 3!")
                self.LOGGER(__name__).warning(f"Check FSUB_CHANNEL3 ({FSUB_CHANNEL3}) and ensure the bot is admin with invite permissions.")
                sys.exit()

        if FSUB_ENABLED4 and FSUB_CHANNEL4:
            try:
                link = (await self.get_chat(FSUB_CHANNEL4)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_CHANNEL4)
                    link = (await self.get_chat(FSUB_CHANNEL4)).invite_link
                self.invitelink4 = link
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning("Failed to export invite link for Fsub channel 4!")
                self.LOGGER(__name__).warning(f"Check FSUB_CHANNEL4 ({FSUB_CHANNEL4}) and ensure the bot is admin with invite permissions.")
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
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/rohit_1888")
        print("Welcome to Bot Modified by Rohit")
        self.username = usr_bot_me.username

        # Web server setup
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")


