import io

import aiohttp
import magic

from fortytwo_transcribe.settings import Settings
from fortytwo_transcribe.types import AIResponse


class OpenAIProvider:
    async def transcribe(self, audio_bytes: io.BytesIO) -> AIResponse:
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {Settings().openai_api_key}"}

        mime = magic.Magic(mime=True)
        content_type = mime.from_buffer(audio_bytes.getvalue())
        audio_bytes.seek(0)

        data = aiohttp.FormData()
        data.add_field(
            "file",
            audio_bytes.read(),
            content_type=content_type,
        )
        data.add_field("model", "whisper-1")

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.post(url, headers=headers, data=data) as resp:
                response = await resp.json()

                return AIResponse(
                    content=response['text'],
                    provider="OPENAI",
                )
