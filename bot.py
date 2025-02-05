import asyncio
import logging
import sys
import os
from aiohttp import web
from datetime import datetime
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
from plugins import web_server
from config import *

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Set port for web server
PORT = int(os.getenv("PORT", 8080))  # Default to 8080 if not set


class Bot(Client):
    def __init__(self):
        """Initialize bot with configuration"""
        super().__init__(
            name="FileStore",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
            parse_mode=ParseMode.HTML
        )
        self.LOGGER = logging
        self.start_time = datetime.now()

    async def start(self):
        """Start the bot and initialize required components"""
        await super().start()
        self.me = await self.get_me()
        self.username = self.me.username
        self.uptime = datetime.now()

        # Initialize force sub channels
        await self.init_force_sub_channels()

        # Initialize database channel
        await self.init_db_channel()

        # Start web server
        asyncio.create_task(self.start_web_server())

        # Send startup notification
        try:
            await self.send_message(
                OWNER_ID,
                f"<b>🤖 Bot Started Successfully!</b>\n\n"
                f"<b>Bot:</b> {self.me.mention}\n"
                f"<b>Support:</b> @cosmic_freak"
            )
        except Exception as e:
            self.LOGGER.warning(f"Failed to send startup notification: {e}")

    async def init_force_sub_channels(self):
        """Initialize force subscription channels and their invite links"""
        force_sub_channels = [FORCE_SUB_CHANNEL1, FORCE_SUB_CHANNEL2, FORCE_SUB_CHANNEL3, FORCE_SUB_CHANNEL4]
        self.force_sub_links = {}

        for channel_id in force_sub_channels:
            if channel_id:
                try:
                    chat = await self.get_chat(channel_id)
                    invite_link = chat.invite_link or await self.export_chat_invite_link(channel_id)
                    self.force_sub_links[channel_id] = invite_link
                except Exception as e:
                    self.LOGGER.error(f"Error initializing force sub channel {channel_id}: {e}")

    async def init_db_channel(self):
        """Initialize database channel and check if bot has permission to send messages"""
        try:
            channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = channel
            test_message = await self.send_message(channel.id, "Test Message")
            await test_message.delete()
        except Exception as e:
            self.LOGGER.error(f"Error initializing DB channel: {e}")

    async def start_web_server(self):
        """Start a simple web server for health checks"""
        try:
            app = web.AppRunner(await web_server())
            await app.setup()
            site = web.TCPSite(app, "0.0.0.0", PORT)
            await site.start()
            self.LOGGER.info(f"✅ Web server started on port {PORT}")
        except Exception as e:
            self.LOGGER.error(f"❌ Web server failed to start: {e}")

    async def stop(self, *args):
        """Stop the bot gracefully"""
        await super().stop()
        self.LOGGER.info("Bot stopped.")

    def run(self):
        """Run the bot with proper error handling"""
        self.LOGGER.info("Starting bot...")
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start())
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER.info("Stopping bot...")
        finally:
            loop.run_until_complete(self.stop())
            self.LOGGER.info("Bot stopped successfully!")