from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # A single URL takes precedence over the individual DB_* variables.
    # This is what Railway, Docker and managed database providers expose.
    DATABASE_URL: str | None = None

    # Optional DDL user for Alembic. Falls back to DATABASE_URL when omitted.
    MIGRATION_DATABASE_URL: str | None = None

    # Database variables (fallback for local development)
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str | None = None

    # JWT variables
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if not (self.DB_USER and self.DB_PASSWORD and self.DB_NAME):
            raise ValueError(
                "Set DATABASE_URL or all of DB_USER, DB_PASSWORD and DB_NAME."
            )
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def migration_database_url(self) -> str:
        return self.MIGRATION_DATABASE_URL or self.database_url

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
