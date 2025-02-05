from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
#rohit_1888 on Tg
from config import *


name ="""
 BY CODEFLIX BOTS
"""


class Bot(Client):
    def __init__(self):
        """Initialize bot with configuration"""
        super().__init__(
            name="FileStore",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER
        self.start_time = datetime.now()

    async def start(self):
        """Start the bot and initialize required variables"""
        await super().start()
        self.me = await self.get_me()
        self.username = self.me.username
        self.uptime = datetime.now()

        # Initialize force sub channels
        await self.init_force_sub_channels()
        
        # Initialize database channel
        await self.init_db_channel()
        
        # Start web server
        await self.start_web_server()
        
        # Send startup notification
        try:
            await self.send_message(
                OWNER_ID,
                f"<b>🤖 Bot Started Successfully!</b>\n\n"
                f"<b>Bot:</b> {self.me.mention}\n"
                f"<b>Support:</b> @cosmic_freak"
            )
        except Exception as e:
            self.LOGGER(__name__).warning(f"Failed to send startup notification: {e}")

    async def init_force_sub_channels(self):
        """Initialize force sub channels and their invite links"""
        channels = [
            (FORCE_SUB_CHANNEL1, 'invitelink1'),
            (FORCE_SUB_CHANNEL2, 'invitelink2'),
            (FORCE_SUB_CHANNEL3, 'invitelink3'),
            (FORCE_SUB_CHANNEL4, 'invitelink4')
        ]
        
        for channel_id, attr_name in channels:
            if channel_id:
                try:
                    chat = await self.get_chat(channel_id)
                    invite_link = chat.invite_link or await self.export_chat_invite_link(channel_id)
                    setattr(self, attr_name, invite_link)
                except Exception as e:
                    self.LOGGER(__name__).error(f"Error initializing force sub channel {channel_id}: {e}")
                    sys.exit(1)

    async def init_db_channel(self):
        """Initialize database channel"""
        try:
            channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = channel
            test = await self.send_message(channel.id, "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).error(f"Error initializing DB channel: {e}")
            sys.exit(1)

    async def start_web_server(self):
        """Start the web server for health checks"""
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

    async def stop(self, *args):
        """Stop the bot gracefully"""
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    def run(self):
        """Run the bot with proper error handling"""
        self.LOGGER(__name__).info("Starting bot...")
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start())
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("Stopping bot...")
        finally:
            loop.run_until_complete(self.stop())
            self.LOGGER(__name__).info("Bot stopped successfully!")

     #@rohit_1888 on Tg
