from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Esto calcula automáticamente la ruta raíz de tu proyecto (E-commerce/)
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Database Variables
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str

    # JWT Variables
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Apuntamos directamente a la ruta absoluta del .env
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", 
        extra="ignore",
        case_sensitive=False
    )

settings = Settings()