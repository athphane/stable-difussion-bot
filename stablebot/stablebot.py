import ast
import os
import sys
from configparser import ConfigParser
from functools import wraps
from typing import BinaryIO, List, Optional, Union

import psutil
from pyrogram import Client, types
from pyrogram.raw.all import layer
from pyrogram.types import CallbackQuery, Message


class StableBot(Client):
    def __init__(self, version='0.0.0'):
        self.version = version
        self.name = self.__class__.__name__.lower()
        config_file = 'config.ini'

        self.config = config = ConfigParser()
        config.read(config_file)

        super().__init__(
            'stablebot',
            api_id=config.get('pyrogram', 'api_id'),
            api_hash=config.get('pyrogram', 'api_hash'),
            bot_token=config.get('pyrogram', 'bot_token'),
            workers=16,
            plugins=dict(root="stablebot/plugins"),
            workdir="./"
        )

    def __str__(self):
        """
        String representation of the class object
        """
        return self.__class__.__name__

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"{self.__class__.__name__} v{self.version} (Layer {layer}) started on @{me.username}.\n"
              f"Time to generate all the diffusions.")

    async def stop(self, *args):
        """
        Stop function
        :param args:
        """
        await super().stop()
        print(f"{self.__class__.__name__} stopped. Bye.")

    async def restart(self, git_update=False, pip=False, *args):
        """
        Restart the bot for reals.
        :return:
        """
        await self.stop()

        try:
            c_p = psutil.Process(os.getpid())
            for handler in c_p.open_files() + c_p.connections():
                os.close(handler.fd)
        except Exception as c_e:
            print(c_e)

        if git_update:
            os.system('git pull')
        if pip:
            os.system('pip install -r requirements.txt')

        os.execl(sys.executable, sys.executable, '-m', self.__class__.__name__.lower())
        sys.exit()

    def admins(self):
        return ast.literal_eval(self.config.get(self.name, 'admins'))

    def is_admin(self, entity: Message or CallbackQuery) -> bool:
        user_id = entity.from_user.id

        return user_id in self.admins()

    @staticmethod
    def admins_only(func):
        @wraps(func)
        async def decorator(bot: StableBot, message: Message):
            if bot.is_admin(message):
                await func(bot, message)

        decorator.admin = True

        return decorator

    async def send_log(
            self,
            text: str,
            parse_mode: Optional[str] = object,
            entities: List["types.MessageEntity"] = None,
            disable_web_page_preview: bool = None,
            disable_notification: bool = None,
            reply_to_message_id: int = None,
            schedule_date: int = None,
            reply_markup: Union[
                "types.InlineKeyboardMarkup",
                "types.ReplyKeyboardMarkup",
                "types.ReplyKeyboardRemove",
                "types.ForceReply"
            ] = None
    ) -> Union["types.Message", None]:
        """ Send Message to log group. """
        chat_id = self.config.get(self.name, 'log_group', fallback=None)

        if chat_id:
            return await self.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, entities=entities,
                                           disable_web_page_preview=disable_web_page_preview,
                                           disable_notification=disable_notification,
                                           reply_to_message_id=reply_to_message_id, schedule_date=schedule_date,
                                           reply_markup=reply_markup)

        return None

    async def send_log_document(
            self,
            document: Union[str, BinaryIO],
            thumb: Union[str, BinaryIO] = None,
            caption: str = "",
            parse_mode: Optional[str] = object,
            caption_entities: List["types.MessageEntity"] = None,
            file_name: str = None,
            force_document: bool = None,
            disable_notification: bool = None,
            reply_to_message_id: int = None,
            schedule_date: int = None,
            reply_markup: Union[
                "types.InlineKeyboardMarkup",
                "types.ReplyKeyboardMarkup",
                "types.ReplyKeyboardRemove",
                "types.ForceReply"
            ] = None,
            progress: callable = None,
            progress_args: tuple = ()
    ) -> Union["types.Message", None]:
        """ Send Message to log group. """
        chat_id = self.config.get(self.name, 'log_group', fallback=None)

        if chat_id:
            return await self.send_document(chat_id=chat_id, document=document, thumb=thumb, caption=caption,
                                            caption_entities=caption_entities, file_name=file_name,
                                            force_document=force_document, parse_mode=parse_mode,
                                            reply_to_message_id=reply_to_message_id, schedule_date=schedule_date,
                                            reply_markup=reply_markup, progress=progress, progress_args=progress_args)

        return None
