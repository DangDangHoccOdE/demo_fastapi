import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Default Project"
    SECRET_KEY: str = "defaultsecret"
    DATABASE_URL: str = "sqlite:///./test.db"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../.env"),  # Chỉ định đúng vị trí file .env
        env_ignore_empty = True,
        extra = "ignore",
    )

# Chỉ khởi tạo khi được gọi
settings: Settings = None

def get_settings():
    global settings
    if not settings:
        settings = Settings()
    return settings