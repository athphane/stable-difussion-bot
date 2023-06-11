from pyrogram import filters
from pyrogram.types import Message

from stablebot import StableBot


@StableBot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply(
        'Welcome to StableBot. A Telegram Bot made to interact with Automatic1111/stable-diffusion-webui'
    )
