from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "DevSecOps Copilot"
    GOOGLE_API_KEY: str
    REDIS_URL: str = "redis://localhost:6379/0"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/copilot_db"

    class Config:
        env_file = ".env"

settings = Settings()