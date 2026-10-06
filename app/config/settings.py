from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GROQ_API_KEY: str
    TAVILY_API_KEY: str | None = None

    ALLOWED_MODEL_NAMES: list[str] = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b"
    ]

    class Config:
        env_file = ".env"


settings = Settings()