from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=["../.env.dev", "../src/.env.secret"],
        env_file_encoding="utf-8",
    )
    host: str
    user: str
    password: str
    db: str
    port: int
    url: str


settings = Settings()  # type: ignore

if __name__ == "__main__":
    print(settings)
