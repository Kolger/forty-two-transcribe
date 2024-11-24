import asyncio
import io
import tempfile

import telegram
from moviepy import VideoFileClip

from fortytwo_transcribe.logger import logger
from fortytwo_transcribe.openai import OpenAIProvider
from fortytwo_transcribe.types import AIResponse


class Manager:
    async def __extract_audio(self, video_bytes: io.BytesIO) -> io.BytesIO:
        loop = asyncio.get_event_loop()

        def process_video() -> io.BytesIO:
            with tempfile.NamedTemporaryFile(delete=True) as video_file:
                video_file.write(video_bytes.getvalue())
                video_file.seek(0)
                with VideoFileClip(video_file.name) as video:
                    audio = video.audio
                    audio_buffer = io.BytesIO()
                    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as audio_file:
                        audio.write_audiofile(audio_file.name, codec='mp3', logger=None)
                        audio_buffer.write(audio_file.read())
                    audio_buffer.seek(0)
                    return audio_buffer

        return await loop.run_in_executor(None, process_video)

    async def transcribe_video(self, video_file: telegram.File) -> AIResponse:
        bytes_buffer = io.BytesIO()
        await video_file.download_to_memory(out=bytes_buffer)
        bytes_buffer.seek(0)
        audio_bytes_io = await self.__extract_audio(bytes_buffer)

        return await self.__transcribe_bytes(audio_bytes_io)

    async def transcribe_audio(self, audio_file: telegram.File) -> AIResponse:
        audio_bytes = await audio_file.download_as_bytearray()
        audio_bytes_io = io.BytesIO(audio_bytes)

        return await self.__transcribe_bytes(audio_bytes_io)

    async def __transcribe_bytes(self, audio_bytes: io.BytesIO) -> AIResponse:
        openai_provider = OpenAIProvider()
        try:
            return await openai_provider.transcribe(audio_bytes)
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}, exception type: {e.__class__.__name__}")
            return AIResponse(content=f"Error while transcribing audio: {str(e)}", provider="OPENAI", error=True)
