from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import asyncio

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

# Initialize rate limit data for users (in-memory dictionary for rate limiting)
user_rate_limits = {}

# Function to check rate limit
def check_rate_limit(user_id):
    current_time = asyncio.get_event_loop().time()
    if user_id in user_rate_limits:
        last_request_time = user_rate_limits[user_id]
        # 8 hours in seconds
        if current_time - last_request_time < 28800:  # 8 hours
            return False, 28800 - (current_time - last_request_time)  # Returns False and time remaining
    return True, 0

# Function to update rate limit for user
def update_rate_limit(user_id):
    user_rate_limits[user_id] = asyncio.get_event_loop().time()

# `/id` Command: Get User ID and Info
@Bot.on_message(filters.command("id") & filters.private)
async def showid(client, message: Message):
    user_id = message.chat.id
    first_name = message.chat.first_name
    username = message.chat.username or "No username"

    # Check rate limit for the user
    rate_limit_ok, time_remaining = check_rate_limit(user_id)
    
    if not rate_limit_ok:
        hours = time_remaining // 3600
        minutes = (time_remaining % 3600) // 60
        seconds = time_remaining % 60
        await message.reply_text(
            f"⏳ You can request again in {hours}h {minutes}m {seconds}s.",
            quote=True,
        )
        return

    # Update rate limit for user (this will be used the next time they request)
    update_rate_limit(user_id)

    # Prepare the message with user information and buttons
    response = f"""
    👤 <b>Your Profile Information</b>:
    • <b>Full Name:</b> {first_name}
    • <b>Username:</b> @{username}
    • <b>User ID:</b> <code>{user_id}</code>
    
    ✨ All your info has been retrieved successfully!
    """

    # Inline Keyboard with a button to show profile details
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 View Profile", callback_data="profile")]
    ])
    
    # Send the profile information with button
    await message.reply_text(response, reply_markup=reply_markup, quote=True)

# Callback Query Handler for the "Profile" Button
@Bot.on_callback_query()
async def cb_handler(client, query):
    data = query.data
    if data == "profile":
        # Delete the previous message to make things clean and smooth
        await query.message.delete()

        # Prepare detailed user profile information (can be extended)
        user_id = query.from_user.id
        first_name = query.from_user.first_name
        username = query.from_user.username or "No username"
        bio = query.from_user.bio or "No bio available"

        profile_message = f"""
        🖼️ <b>Your Profile</b>:
        
        • <b>Full Name:</b> {first_name}
        • <b>Username:</b> @{username}
        • <b>User ID:</b> <code>{user_id}</code>
        • <b>Bio:</b> {bio}
        
        """

        # Send the profile info again
        await query.message.reply_text(profile_message, reply_markup=None, quote=True)

        # Optionally add a button for future reference or action (like settings)
        await query.message.reply_text(
            "You can always view or edit your profile here! 😊",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Refresh Profile", callback_data="profile"),
                 InlineKeyboardButton("❌ Exit", callback_data="exit")]
            ])
        )

    # Handle the Exit button (deletes the message when clicked)
    elif data == "exit":
        # Delete the current profile message
        await query.message.delete()
