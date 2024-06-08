import os
from typing import Optional

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
    host: Optional[str]
    user: Optional[str]
    password: Optional[str]
    db: Optional[str]
    port: Optional[int]
    url: Optional[str]


settings = Settings()  # type: ignore
