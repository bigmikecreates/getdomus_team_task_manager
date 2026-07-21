from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/taskmanager"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
