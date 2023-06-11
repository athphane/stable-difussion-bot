import asyncio
import os

from pyrogram import filters, enums
from pyrogram.types import Message, InputMediaPhoto

from stablebot import StableBot
from stablebot.stable_difussion.api import StableDiffusion


@StableBot.on_message(filters.command(['gen', 'generate', 'txt2img']))
async def base_text_to_image(_, message: Message):
    response_message = await message.reply('Generating your prompt...')

    await message.reply_chat_action(enums.ChatAction.TYPING)

    if len(message.command) == 3:
        prompt = message.command[1]
        steps = int(message.command[2])
        images = StableDiffusion().generate_image(prompt, steps)
    else:
        prompt = ' '.join(message.command[1:])
        steps = 10
        images = StableDiffusion().generate_image(prompt, steps)

    with open('activity.csv', 'a+') as activity:
        activity_string = f"{message.from_user.id},{message.from_user.username},{prompt},{steps}\n"
        activity.write(activity_string)

    await message.reply_chat_action(enums.ChatAction.TYPING)

    message_images = []
    for image in images:
        message_images.append(InputMediaPhoto(image, caption=prompt))

    await message.reply_chat_action(enums.ChatAction.UPLOAD_PHOTO)

    await asyncio.gather(
        message.reply_media_group(message_images),
        response_message.delete()
    )

    for image in images:
        os.remove(image)
