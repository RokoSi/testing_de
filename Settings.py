from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env.dev", "../src/.env.secret"),
        env_file_encoding="utf-8",
    )

    host: str
    user: str
    password: str
    db: str
    URL: str
