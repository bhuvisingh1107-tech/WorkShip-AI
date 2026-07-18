from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment configuration placeholders for the backend."""

    PROJECT_NAME: str = "WorkShip AI API"
    API_VERSION: str = "0.1.0"
    DATABASE_URL: str = ""
    OPENAI_API_KEY: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
