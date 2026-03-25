from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic  import Field

class Settings(BaseSettings):
    GROQ_API_KEY: str
    GROQ_MODEL: str
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str

    MATCH_THRESHOLD: float 
    MATCH_COUNT: int 

    model_config = SettingsConfigDict(env_file=".env",extra="ignore")

CONFIG = Settings()