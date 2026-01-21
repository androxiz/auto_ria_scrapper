import aiohttp
from lxml import html
from urllib.parse import urljoin
from app.utils import parse_odometer, parse_int, parse_phone


class CarDetailScraper:

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def scrape(self, url: str) -> dict | None:
        async with self.session.get(url) as response:
            text = await response.text()

        tree = html.fromstring(text)

        try:
            # New auto
            if "/newauto/" in url:
                title_xpath = '//div[contains(@class,"auto-head")]//h1//strong/text()'
                price_xpath = '//div[contains(@class,"auto-price")]//strong[contains(@class,"price_value")]/text()'
                username_xpath = '//div[contains(@class,"seller_info_name")]//a//strong//span/text()'
                phone_xpath = '//span[contains(@class,"conversion_phone_newcars")]/text()'
                image_xpath = '//picture//img/@src'
                images_count_xpath = '//div[contains(@class,"panoram-tab")]//label[contains(@class,"panoram-tab-item")]/text()'
                car_vin_xpath = '//div[@class="badge-template"]//span[contains(@class,"badge")]/text()'
            else:
                # Old auto
                title_xpath = '//div[@id="sideTitleTitle"]//span/text() | //h1.head/text() | //h3.auto-content_title/text()'
                price_xpath = '//div[@id="basicInfoPrice"]//strong/text() | //div[@id="sidePrice"]//strong/text() | //div[contains(@class,"price_value")]/strong/text()'
                username_xpath = '//div[@id="sellerInfoUserName"]//span/text() | //a[@class="sellerPro"]/text() | //div[@class="seller_info_name"]/a/text()'
                phone_xpath = '//button[@class="size-large conversion" and @data-action="showBottomPopUp"]//span/text()'
                image_xpath = '//span[@class="picture"]//img/@src | //div[contains(@class,"photo-620x465")]//img/@src'
                images_count_xpath = '//span[contains(@class,"common-badge")]/span[2]/text() | //a[@class="show-all"]/text()'
                car_vin_xpath = '//span[@id="badgesVin"]//span/text() | //span[contains(@class,"vin-code")]/text()'

            return {
                "url": url,
                "title": self._get(tree, title_xpath) or "Unknown",
                "price_usd": parse_int(self._get(tree, price_xpath)) or 0,
                "odometer": parse_odometer(self._get(tree, '//div[contains(@id,"basicInfoTableMainInfo")]//span/text()')) or 0,
                "username": self._get(tree, username_xpath) or "Unknown",
                "phone_number": parse_phone(self._get(tree, phone_xpath)) or "Unknown",
                "image_url": self._get(tree, image_xpath) or "Unknown",
                "images_count": parse_int(self._get(tree, images_count_xpath)) or 1,
                "car_number": self._get(tree, '//div[contains(@class,"car-number")]/span/text()') or "Unknown",
                "car_vin": self._get(tree, car_vin_xpath) or "Unknown",
            }
        except Exception as e:
            print(f"[ERROR] scraping {url}: {e}")
            return None

    def _get(self, tree, xpath: str):
        result = tree.xpath(xpath)
        return result[0].strip() if result else None
