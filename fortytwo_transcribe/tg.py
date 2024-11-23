import asyncio
import io

from telegram import Update, constants

from telegram.ext import Application, ContextTypes, MessageHandler, filters

from fortytwo_transcribe.manager import Manager
from fortytwo_transcribe.settings import Settings
from typing import Coroutine
from fortytwo_transcribe.types import AIResponse

class TelegramBot:
    def __init__(self, token: str = None):
        if not token:
            token = Settings().telegram_token
        self.token = token
        self.manager = Manager()
        self.application = Application.builder().token(self.token).concurrent_updates(True).build()
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        self.application.add_handler(MessageHandler(filters.VIDEO_NOTE, self.handle_video_note))
        self.application.add_handler(MessageHandler(filters.VIDEO, self.handle_video))
        self.application.add_handler(MessageHandler(filters.AUDIO, self.handle_audio))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        self.application.add_handler(MessageHandler(~filters.TEXT & ~filters.VIDEO_NOTE & ~filters.VIDEO & ~filters.AUDIO & ~filters.VOICE, self.handle_other))

    async def handle_other(self, tg_update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.__send_message(tg_update, "Sorry, I cannot process this message")

    async def handle_text(self, tg_update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = tg_update.message.text
        await self.__send_message(tg_update, f"Sorry, I cannot process this message:\n{text}")

    async def handle_voice(self, tg_update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        audio_file = await tg_update.message.voice.get_file()
        message = await self.__execute_with_typing(self.manager.transcribe_audio(audio_file), tg_update)

        if message:
            await self.__send_message(tg_update, message.content)

    async def handle_audio(self, tg_update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        audio_file = await tg_update.message.audio.get_file()
        message = await self.__execute_with_typing(self.manager.transcribe_audio(audio_file), tg_update)

        if message:
            await self.__send_message(tg_update, message.content)

    async def handle_video_note(self, tg_update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        video_file = await tg_update.message.video_note.get_file()
        message = await self.__execute_with_typing(self.manager.transcribe_video(video_file), tg_update)

        if message:
            await self.__send_message(tg_update, message.content)

    async def handle_video(self, tg_update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        video_file = await tg_update.message.video.get_file()
        message = await self.__execute_with_typing(self.manager.transcribe_video(video_file), tg_update)

        if message:
            await self.__send_message(tg_update, message.content)

    async def __send_message(self, tg_update: Update, message: str):
        if len(message) < constants.MessageLimit.MAX_TEXT_LENGTH:
            await tg_update.message.reply_text(message, reply_to_message_id=tg_update.message.message_id)
        else:
            bytes_buffer = io.BytesIO(message.encode('utf-8'))
            bytes_buffer.name = 'transcription.txt'
            await tg_update.message.reply_document(
                document=bytes_buffer,
                filename='transcription.txt',
                caption='Transcription',
            reply_to_message_id=tg_update.message.message_id
        )

    async def __execute_with_typing(self, coro: Coroutine, tg_update: Update) -> AIResponse | bool:
        async def show_typing():
            while True:
                await self.application.bot.send_chat_action(tg_update.message.chat.id, 'typing')
                await asyncio.sleep(2)

        try:
            typing_task = asyncio.create_task(show_typing())
            result = await asyncio.wait_for(coro, timeout=60)
            typing_task.cancel()
            return result
        except asyncio.TimeoutError:
            typing_task.cancel()
            await self.application.bot.send_message(tg_update.message.chat.id, "The operation took too long and was canceled.")
            return False

    def run(self) -> None:
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
