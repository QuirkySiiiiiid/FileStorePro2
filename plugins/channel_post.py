import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to generate and return inline keyboard for sharing URL
def create_inline_keyboard(link):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'id','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    """
    Handles private messages from admins. Copies the message to a channel, 
    generates a start link, and sends it back to the admin with a share button.
    """
    # Sending a "Please Wait" message while processing
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    
    try:
        # Attempt to copy the message to the designated channel
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        # If a FloodWait error occurs, wait for the required time and retry
        logger.info(f"Flood wait detected. Sleeping for {e.x} seconds.")
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        # Log the error and notify the admin if something goes wrong
        logger.error(f"Error copying message to channel: {e}")
        await reply_text.edit_text("Something went wrong..! Please try again.")
        return

    # Create a unique string for the start link based on the post message ID
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    
    # Encode the string to base64
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    
    # Create inline keyboard with the share URL button
    reply_markup = create_inline_keyboard(link)

    # Send the link to the admin with a "share URL" button
    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    # If the channel button isn't disabled, update the original post with the same "share URL" button
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)
    
    # Log the successful processing of the message
    logger.info(f"Successfully processed the post for admin {message.from_user.id}. Link: {link}")
