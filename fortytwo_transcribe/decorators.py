from fortytwo_transcribe.settings import Settings
from fortytwo_transcribe.logger import logger
from telegram import Update
from telegram.ext import ContextTypes


def check_access(func):
    async def wrapper(self, tg_update: Update, context: ContextTypes.DEFAULT_TYPE):
        allowed_users_list = Settings().allowed_users
        
        if allowed_users_list and (
            tg_update.message.chat.username not in allowed_users_list and 
            tg_update.message.chat.id not in allowed_users_list
        ):
            logger.info(f"User {tg_update.message.chat.username} with id {tg_update.message.chat.id} is not allowed to use this bot")
            await context.bot.send_message(tg_update.message.chat.id, "You are not allowed to use this bot, please contact the administrator")
            return False

        return await func(self, tg_update, context)

    return wrapper