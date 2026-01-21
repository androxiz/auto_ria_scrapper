import aiohttp
import asyncio
from app.scrapers.listing import ListingScraper
from app.scrapers.detail import CarDetailScraper
from app.repositories.car_repository import CarRepository
from app.config import settings

SEM = asyncio.Semaphore(10)

class ScraperService:

    async def run(self):
        async with aiohttp.ClientSession(
            headers={"User-Agent": "Mozilla/5.0"}
        ) as session:

            listing = ListingScraper(session)
            detail = CarDetailScraper(session)

            page = 1
            has_next = True

            while has_next:
                page_url = f"{settings.START_URL}?page={page}"
                print(f"\n[PAGE] Scraping page {page} -> {page_url}")

                urls, has_next = await listing.get_car_urls(page_url)

                saved_count = 0
                skipped_count = 0

                for url in urls:
                    result = await self.process_car(detail, url)
                    if result == "saved":
                        saved_count += 1
                    elif result == "skip":
                        skipped_count += 1

                print(f"[PAGE SUMMARY] Page {page}: {saved_count} saved, {skipped_count} skipped")
                page += 1

    async def process_car(self, detail: CarDetailScraper, url: str):
        async with SEM:
            if await CarRepository.exists(url):
                print(f"[SKIP] Duplicate found: {url}")
                return "skip"

            data = await detail.scrape(url)
            if data:
                await CarRepository.create(data)
                title = data.get("title", "Unknown")
                price = data.get("price_usd", "Unknown")
                odometer = data.get("odometer", "Unknown")
                print(f"[SAVED] {title} | Price: {price} USD | Odometer: {odometer} km")
                return "saved"
