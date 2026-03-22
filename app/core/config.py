from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic  import Field

class Settings(BaseSettings):
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
    GROQ_MODEL: str = Field(..., env="GROQ_MODEL")
    SUPABASE_URL: str = Field(..., env="SUPABASE_URL")
    SUPABASE_SERVICE_KEY: str = Field(..., env="SUPABASE_SERVICE_KEY")

    MATCH_THRESHOLD: float = Field(0.7, env="MATCH_THRESHOLD")
    MATCH_COUNT: int = Field(5, env="MATCH_COUNT")

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

CONFIG = Settings()