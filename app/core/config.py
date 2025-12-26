from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/radar"

    # Fuentes (puedes cambiarlas luego)
    rss_sources: list[str] = [
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "https://remotive.com/remote-jobs/software-dev/rss",

        # We Work Remotely (general + categorías útiles)
        "https://weworkremotely.com/remote-jobs.rss",
        "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",

        # Remotive (feed general)
        "https://remotive.com/feed",

        # Himalayas (feed público)
        "https://himalayas.app/jobs/rss",

        # JobsCollider (categoría software dev, remote)
        "https://jobscollider.com/remote-software-development-jobs.rss",

        # Jobicy (feed “generator”: puedes filtrar por keyword / industria)
        "https://jobicy.com/feed/job_feed",
    ]

    class Config:
        env_file = ".env"

settings = Settings()
