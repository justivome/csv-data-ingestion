from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            "../.env.example",  # Root .env.example (fallback defaults)
            "../.env",  # Root .env
            ".env",  # Local backend/.env (highest priority)
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # PostgreSQL username
    postgres_user: str
    # PostgreSQL password
    postgres_password: str
    # PostgreSQL host
    postgres_host: str = "localhost"
    # PostgreSQL port
    postgres_port: int = 5432
    # PostgreSQL database name
    postgres_db: str

    @property
    def postgres_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


db = DatabaseSettings()
