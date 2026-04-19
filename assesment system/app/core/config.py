from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    APP_NAME: str = "AI Assessment Platform"
    ENV: str = "development"
    DEBUG: bool = True

    OPENAI_API_KEY: str

    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ai_db"
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("OPENAI_API_KEY")
    def validate_openai_key(cls, value):
        if not value or value == "your_api_key_here":
            raise ValueError("OPENAI_API_KEY is required and must be set in .env")
        return value


settings = Settings()