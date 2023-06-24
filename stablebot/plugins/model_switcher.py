from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from stablebot import StableBot, custom_filters
from stablebot.stable_difussion.api import StableDiffusion


@StableBot.on_message(filters.command(['models', 'switch']))
async def model_switcher_command(_, message: Message):
    raw_models = StableDiffusion().get_models()

    available_models = []
    for raw_model in raw_models:
        details = {
            'title': raw_model['title'],
            'model_name': raw_model['model_name']
        }
        available_models.append(details)

    buttons = []
    for model in available_models:
        buttons.append([InlineKeyboardButton(text=model['title'], callback_data=f"switch_model+{model['model_name']}")])

    await message.reply('Select a model you want to switch SD to...', reply_markup=InlineKeyboardMarkup(buttons))


@StableBot.on_callback_query(custom_filters.callback_query('switch_model'), group=2)
async def switch_model_callback(bot: StableBot, callback: CallbackQuery):
    await callback.answer()

    selected_model = callback.payload

    await callback.message.reply_chat_action(enums.ChatAction.TYPING)
    await callback.message.edit('Switching models. This may take a while...')

    await callback.message.reply_chat_action(enums.ChatAction.TYPING)
    success = StableDiffusion().change_model(selected_model)

    if success:
        await callback.message.reply(f"SD model changed to \"{selected_model}\" successfully.")
    else:
        await callback.message.reply("Something went wrong. Please check SD Console for more information.")

