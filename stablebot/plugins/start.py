import os

from pyrogram import filters
from pyrogram.types import Message

from stablebot import StableBot


@StableBot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply(
        'Welcome to StableBot. A Telegram Bot made to interact with Automatic1111/stable-diffusion-webui'
    )


@StableBot.on_message(filters.command("history") & filters.user([352665135]))
async def send_history_file(_, message: Message):
    await message.reply_document('activity.csv')


@StableBot.on_message(filters.command("seturl") & filters.user([352665135]))
async def set_sd_url(_, message: Message):
    the_url = ''.join(message.command[1:])
    os.environ['SD_URL'] = the_url
    await message.reply(f'SD URL set to:\n{the_url}')


@StableBot.on_message(filters.command("geturl") & filters.user([352665135]))
async def get_sd_url(_, message: Message):
    await message.reply(f"'SD URL currently:\n{os.environ['SD_URL']}'")
