from pyrogram import Client
from bot import Bot
from config import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import add_user, del_user, full_userbase, present_user

# Function to create inline keyboards
def create_inline_keyboard(buttons):
    """
    Helper function to generate an InlineKeyboardMarkup with the provided buttons.
    It takes a list of button rows, where each row is a list of tuples (button_text, callback_data).
    """
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=data) for text, data in row] for row in buttons])

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    """
    Handles callback queries triggered by users clicking inline buttons in messages.
    Depending on the callback data, it updates the message with the relevant content.
    """
    try:
        data = query.data  # Retrieve the callback data from the query

        if data == "help":
            # If the callback data is "help", send a help message with buttons
            await query.message.edit_text(
                text=HELP_TXT.format(first=query.from_user.first_name),  # Format the help message with user's first name
                disable_web_page_preview=True,
                reply_markup=create_inline_keyboard([['ʜᴏᴍᴇ', 'start'], ['ᴄʟᴏꜱᴇ', 'close']])  # Buttons for Home and Close
            )
        elif data == "about":
            # If the callback data is "about", send an about message with buttons
            await query.message.edit_text(
                text=ABOUT_TXT.format(first=query.from_user.first_name),  # Format the about message with user's first name
                disable_web_page_preview=True,
                reply_markup=create_inline_keyboard([['ʜᴏᴍᴇ', 'start'], ['ᴄʟᴏꜱᴇ', 'close']])  # Buttons for Home and Close
            )
        elif data == "start":
            # If the callback data is "start", send a welcome/start message with buttons
            await query.message.edit_text(
                text=START_MSG.format(first=query.from_user.first_name),  # Format the start message with user's first name
                disable_web_page_preview=True,
                reply_markup=create_inline_keyboard([['ʜᴇʟᴘ', 'help'], ['ᴀʙᴏᴜᴛ', 'about']])  # Buttons for Help and About
            )
        elif data == "close":
            # If the callback data is "close", delete the current message and any reply-to message
            await query.message.delete()  # Delete the current message
            try:
                # Attempt to delete the previous message the user replied to
                await query.message.reply_to_message.delete()
            except Exception as e:
                # If an error occurs while deleting the previous message, log the error
                print(f"Error deleting previous message: {e}")
    
    except Exception as e:
        # If any error occurs in processing the callback query, log the error
        print(f"Error handling callback query: {e}")
