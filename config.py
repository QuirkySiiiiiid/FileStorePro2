

import os
from os import environ, getenv
import logging
from logging.handlers import RotatingFileHandler

# Bot Token from @BotFather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# API Credentials from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

# Database Channel ID for storing files
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))

# Owner Details
OWNER = os.environ.get("OWNER", "Yato")  # Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", ""))  # Owner user ID

# MongoDB Database Configuration
DB_URI = os.environ.get("DATABASE_URL", "")  # MongoDB connection URI
DB_NAME = os.environ.get("DATABASE_NAME", "FileStore")  # Database name

# Auto-Delete Configuration
TIME = int(os.environ.get("TIME", "10"))  # Time in seconds for auto-delete messages

# Force Subscribe Channel Configuration
# Set channel IDs for force subscribe feature (set to 0 to disable)
FORCE_SUB_CHANNEL1 = int(os.environ.get("FORCE_SUB_CHANNEL1", "0"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "0"))
FORCE_SUB_CHANNEL4 = int(os.environ.get("FORCE_SUB_CHANNEL4", "0"))

# Bot Workers
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Random Images for Bot Responses
# Add multiple image URLs for dynamic image changes
PICS = [
    "https://telegra.ph/file/1.jpg",
    "https://telegra.ph/file/2.jpg",
    "https://telegra.ph/file/3.jpg",
    # Add more image URLs here
]

# Default Images
# START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/start.jpg")
# FORCE_PIC = os.environ.get("FORCE_PIC", "https://telegra.ph/file/force.jpg")

# Shortlink Configuration
TOKEN = True if os.environ.get('TOKEN', "True") == "True" else False
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 600))
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "")

# Bot Messages and Captions
HELP_TXT = """<b>» ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs:

›› /batch : ᴄʀᴇᴀᴛᴇ ɢʀᴏᴜᴘ ᴍᴇssᴀɢᴇs
›› /genlink : ᴄʀᴇᴀᴛᴇ ʟɪɴᴋ ғᴏʀ ᴏɴᴇ ᴘᴏsᴛ
›› /broadcast : ʙʀᴏᴀᴅᴄᴀsᴛ ᴍᴇssᴀɢᴇ
›› /broadcast silent : sɪʟᴇɴᴛ ʙʀᴏᴀᴅᴄᴀsᴛ
›› /forcesub : ᴠɪᴇᴡ ғᴏʀᴄᴇsᴜʙ ᴄᴏᴍᴍᴀɴᴅs
›› /users : ᴠɪᴇᴡ ᴜsᴇʀ sᴇᴛᴛɪɴɢs
›› /fsettings : ᴠɪᴇᴡ ғɪʟᴇ sᴇᴛᴛɪɴɢs
›› /autodel : ᴠɪᴇᴡ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ
›› /commands : ᴠɪᴇᴡ ʙᴀsɪᴄ ᴄᴏᴍᴍᴀɴᴅs
›› /restart : ʀᴇsᴛᴀʀᴛ ʙᴏᴛ
›› /stats : ᴠɪᴇᴡ sᴛᴀᴛɪsᴛɪᴄs</b>"""

# About Text with Dynamic Bot Username
ABOUT_TXT = """
›› ᴍʏ ɴᴀᴍᴇ: **__{}__**
›› ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ: Cʟɪᴄᴋ ʜᴇʀᴇ
›› ᴏᴡɴᴇʀ: {OWNER_USERNAME}
›› ʟᴀɴɢᴜᴀɢᴇ: Pʏᴛʜᴏɴ 3
›› ʟɪʙʀᴀʀʏ: Pʏʀᴏɢʀᴀᴍ ᴠ2
›› ᴅᴀᴛᴀʙᴀsᴇ: Mᴏɴɢᴏ ᴅʙ
›› ᴅᴇᴠᴇʟᴏᴘᴇʀ: @cosmic_freak
"""

# Welcome Message Template
START_MSG = """<b>ʜᴇʟʟᴏ {first} 👋

ɪ'ᴍ ᴀ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ ᴡɪᴛʜ ᴇxᴛʀᴀ ғᴇᴀᴛᴜʀᴇs! 🚀

ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴇxᴘʟᴏʀᴇ!</b>"""

# Admin List Configuration
try:
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split()]
    ADMINS.append(OWNER_ID)
except ValueError:
    raise Exception("Invalid admin list. Please check ADMINS environment variable.")

# Force Subscribe Message
FORCE_MSG = """<b>ʜᴇʟʟᴏ {first} 👋

ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ!

ᴄʟɪᴄᴋ ᴏɴ "ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ" ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ 👇</b>"""

# Custom Caption for Files
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>ғɪʟᴇ: {filename}</b>")

# Protection Settings
PROTECT_CONTENT = os.environ.get('PROTECT_CONTENT', "False") == "True"
DISABLE_CHANNEL_BUTTON = os.environ.get('DISABLE_CHANNEL_BUTTON', "False") == "True"

# Statistics Message Template
BOT_STATS_TEXT = """<b>ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs
⌚️ ᴜᴘᴛɪᴍᴇ: {uptime}
👥 ᴜsᴇʀs: {users}
⚡️ ᴄᴘᴜ: {cpu}%
💾 ʀᴀᴍ: {ram}%</b>"""

# Error Messages
USER_REPLY_TEXT = "⚠️ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ!"

# Logging Configuration
LOG_FILE_NAME = "filestore_bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)
   