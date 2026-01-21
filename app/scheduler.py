import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.scraper_service import ScraperService
from app.services.dump_service import dump_database
from app.config import settings

def parse_time(time_str: str):
    hour, minute = map(int, time_str.split(":"))
    return hour, minute

def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")

    scraper_hour, scraper_minute = parse_time(settings.SCRAPER_TIME)
    dump_hour, dump_minute = parse_time(settings.DUMP_TIME)

    async def run_scraper():
        service = ScraperService()
        await service.run()

    scheduler.add_job(
        run_scraper,
        trigger="cron",
        hour=scraper_hour,
        minute=scraper_minute,
        name="daily_scraper"
    )

    scheduler.add_job(
        dump_database,
        trigger="cron",
        hour=dump_hour,
        minute=dump_minute,
        name="daily_dump"
    )

    scheduler.start()
    print("Scheduler started")
