
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

# Custom error message for unauthorized users
NOT_ADMIN_MSG = (
    "🚫 <b>You're not my admin!</b>\n\n"
    "To get admin rights, contact: \n"
    "<blockquote>@Anime106_Request_Bot</blockquote>"
)

@Bot.on_message(filters.private & ~filters.user(ADMINS) & filters.command(['batch', 'genlink']))
async def unauthorized_access(client: Client, message: Message):
    await message.reply_text(NOT_ADMIN_MSG, quote=True, disable_web_page_preview=True)

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="📩 <b>Forward the First Message from DB Channel</b> (with Quotes)\n\n"
                     "or Send the DB Channel Post Link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except asyncio.TimeoutError:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        await first_message.reply("❌ <b>Error:</b> This post is not from my DB Channel.", quote=True)

    while True:
        try:
            second_message = await client.ask(
                text="📩 <b>Forward the Last Message from DB Channel</b> (with Quotes)\n\n"
                     "or Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except asyncio.TimeoutError:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        await second_message.reply("❌ <b>Error:</b> This post is not from my DB Channel.", quote=True)

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"✅ <b>Here is your batch link:</b>\n\n{link}", quote=True, reply_markup=reply_markup)

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(
                text="📩 <b>Forward a Message from the DB Channel</b> (with Quotes)\n\n"
                     "or Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except asyncio.TimeoutError:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        await channel_message.reply("❌ <b>Error:</b> This post is not from my DB Channel.", quote=True)

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"✅ <b>Here is your generated link:</b>\n\n{link}", quote=True, reply_markup=reply_markup)
