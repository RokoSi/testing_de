import os
from typing import Optional, ClassVar

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


env_secret_path = os.path.join(
    os.path.join(os.path.dirname(os.getcwd())), ".env.secret"
)

if not os.path.exists(env_secret_path):
    with open(env_secret_path, "w") as f:
        pass

base_dir = os.path.join(os.path.dirname(os.getcwd()))
load_dotenv(os.path.join(base_dir, ".env.dev"))
load_dotenv(os.path.join(base_dir, ".env.secret"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[
            os.path.join(os.path.join(os.path.dirname(os.getcwd()), ".env.dev")),
            os.path.join(os.path.join(os.path.dirname(os.getcwd()), ".env.secret")),
        ],
        env_file_encoding="utf-8",
    )
    host: Optional[str] = os.getenv("HOST")
    user: Optional[str] = os.getenv("USER")
    password: Optional[str] = os.getenv("PASSWORD")
    db: Optional[str] = os.getenv("DB")
    port_env: ClassVar[Optional[str]] = os.getenv("PORT")
    port: Optional[int] = int(port_env) if port_env is not None else None
    url: Optional[str] = os.getenv("URL")


settings = Settings()
if __name__ == "__main__":
    print(settings)
