from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(... , env="GEMINI_API_KEY")
    GROQ_API_KEY: str = Field(... , env="GROQ_API_KEY")
    GEMINI_MODEL: str = Field(... , env="GEMINI_MODEL")
    GROQ_MODEL: str = Field(... , env="GROQ_MODEL")

    model_config = SettingsConfigDict(env_file=".env")

CONFIG = Settings()