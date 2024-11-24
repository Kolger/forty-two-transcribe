Forty-two Telegram bot that transcribes videos and audio messages to text using the OpenAI Whisper API

Send a video, audio message, or audio file to the bot, and it will transcribe it to text.

## Setup

### 1. Create a .env file with the following content:

```
OPENAI_API_KEY=<your-openai-api-key>
TELEGRAM_API_TOKEN=<your-telegram-api-token>
```

### 2. Run the bot

With docker-compose:

```bash
docker-compose up -d
```

Run without Docker (ffmpeg is required): 

```bash
poetry install
poetry run python main.py
```

## Settings

| Variable           | Description                                                                                        | Default Value |
| ------------------ | -------------------------------------------------------------------------------------------------- | ------------- |
| OPENAI_API_KEY     | OpenAI API key                                                                                     | -             |
| TELEGRAM_API_TOKEN | Telegram API token                                                                                 | -             |
| ALLOWED_USERS      | List of allowed users (username or user id). Should be a Python list. Example: [1234567890, durov] | -             |

## Obtaining API keys

- [Telegram API key](https://core.telegram.org/bots#6-botfather)
- [OpenAI API key](https://beta.openai.com/signup/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Created with love in Barcelona