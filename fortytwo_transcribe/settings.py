from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    openai_api_key: str
    telegram_token: str
    allowed_users: list[int | str] | None = None