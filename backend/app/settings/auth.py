from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "../.env.example",
            "../.env",
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
