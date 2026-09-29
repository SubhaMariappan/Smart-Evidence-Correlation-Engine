from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    """
    Application Settings loaded safely from environment variables or defaults.
    """
    PROJECT_NAME: str = "SECE — Smart Evidence Correlation Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # Forensic Storage Repository Vault Path
    STORAGE_VAULT_DIR: str = "storage/evidence_vault"

    # Security & JWT Token Configuration
    SECRET_KEY: str = "sece_super_secret_key_change_in_production_for_forensic_security"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 Hours

    # PostgreSQL Configuration Variables
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "sece_db"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """Assembles the PostgreSQL connection URI dynamically."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
