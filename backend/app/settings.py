from pydantic import BaseSettings, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Shopify Insights API"
    CORS_ORIGINS: List[AnyHttpUrl] = []
    TIMEOUT_SECONDS: int = 20
    USER_AGENT: str = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    MAX_PAGES: int = 50
    DATABASE_URL: str | None = None  # e.g., mysql+pymysql://user:pass@host:3306/db

    class Config:
        env_file = ".env"

settings = Settings()
