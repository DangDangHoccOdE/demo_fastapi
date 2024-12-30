from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_ignore_empty = True,
        extra = "ignore",
    )

settings = Settings()