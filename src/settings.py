import os

from pydantic_settings import BaseSettings, SettingsConfigDict

env_secret_path = os.path.join(
    os.path.join(os.path.dirname(os.getcwd())), ".env.secret"
)

if not os.path.exists(env_secret_path):
    with open(env_secret_path, "w") as f:
        pass  # Создаем пустой файл


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[
            os.path.join(os.path.join(os.path.dirname(os.getcwd()), ".env.dev")),
            os.path.join(os.path.join(os.path.dirname(os.getcwd()), ".env.secret")),
        ],
        env_file_encoding="utf-8",
    )
    host: str
    user: str
    password: str
    db: str
    port: int
    url: str


settings = Settings()  # type: ignore
