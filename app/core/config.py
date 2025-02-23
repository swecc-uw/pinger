from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pinger"
    VERSION: str = "1.0.0"
    DEV_MODE: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/pinger.db"
    EMAIL_FROM: str = "swecc@uw.edu"
    SENDGRID_API_KEY: str = ""

    MONITOR_INTERVAL: int = 1
    PING_TIMEOUT: float = 1.0

    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()