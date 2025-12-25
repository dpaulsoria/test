from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/radar"

    # Fuentes (puedes cambiarlas luego)
    rss_sources: list[str] = [
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "https://remotive.com/remote-jobs/software-dev/rss",
    ]

    class Config:
        env_file = ".env"

settings = Settings()
