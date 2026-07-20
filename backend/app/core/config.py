from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "WorkShip AI API"
    API_VERSION: str = "0.1.0"
    # Database
    DATABASE_URL: str = "sqlite:///./test.db"
    # Security
    SECRET_KEY: str = "changeme"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # Optional: OpenAI
    OPENAI_API_KEY: str | None = None
    # Supabase
    SUPABASE_URL: str | None = None
    SUPABASE_ANON_KEY: str | None = None
    SUPABASE_JWT_SECRET: str | None = None
    # CORS
    BACKEND_CORS_ORIGINS: str = ""

    model_config = {"case_sensitive": True, "env_file": ".env"}


settings = Settings()