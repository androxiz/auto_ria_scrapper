from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DB_URL = (
        f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('POSTGRES_PORT')}/"
        f"{os.getenv('POSTGRES_DB')}"
    )

    START_URL = os.getenv("START_URL")
    SCRAPER_TIME = os.getenv("SCRAPER_TIME")
    DUMP_TIME = os.getenv("DUMP_TIME")


settings = Settings()