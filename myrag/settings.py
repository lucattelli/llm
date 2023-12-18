from pydantic_settings import BaseSettings, SettingsConfigDict


class Secrets(BaseSettings):
    huggingface_access_token: str
    mongo_uri: str
    openai_api_key: str

    model_config = SettingsConfigDict(env_file=".env.secrets", file_encoding="utf-8")


class Settings(BaseSettings):
    huggingface_embedding_url: str

    model_config = SettingsConfigDict(env_file=".env", file_encoding="utf-8")
