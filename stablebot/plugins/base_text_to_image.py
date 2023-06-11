from pyrogram import filters
from pyrogram.types import Message, InputMediaPhoto

from stablebot import StableBot
from stablebot.stable_difussion.api import StableDiffusion


@StableBot.on_message(filters.command(['gen', 'generate', 'txt2img']))
async def base_text_to_image(_, message: Message):
    if len(message.command) == 3:
        prompt = message.command[1]
        steps = int(message.command[2])
        images = StableDiffusion().generate_image(prompt, steps)
    else:
        prompt = ' '.join(message.command[1:])
        images = StableDiffusion().generate_image(prompt)

    message_images = []
    for image in images:
        message_images.append(InputMediaPhoto(image, caption=prompt))

    await message.reply_media_group(message_images)
