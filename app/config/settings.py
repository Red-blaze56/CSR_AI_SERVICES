from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
    GEMINI_MODEL: str = Field(..., env="GEMINI_MODEL")
    GROQ_MODEL: str = Field(..., env="GROQ_MODEL")
    TOGETHER_API_KEY: str = Field(..., env="TOGETHER_API_KEY")
    TOGETHER_MODEL: str = Field(..., env="TOGETHER_MODEL")
    SUPABASE_URL: str = Field(..., env="SUPABASE_URL")
    SUPABASE_SERVICE_KEY: str = Field(..., env="SUPABASE_SERVICE_KEY")

    model_config = SettingsConfigDict(env_file=".env")


CONFIG = Settings()