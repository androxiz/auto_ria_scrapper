import aiohttp
from lxml import html
from urllib.parse import urljoin

class ListingScraper:

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get_page(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()

    async def get_car_urls(self, page_url: str) -> tuple[list[str], str | None]:
        """
        Returns:
        - a list of links to cars on the current page
        - the URL of the next page (or None if this is the last page)
        """

        html_text = await self.get_page(page_url)
        tree = html.fromstring(html_text)

        links = tree.xpath('//a[contains(@class,"address")]/@href')
        links = [urljoin(page_url, l) for l in links]

        next_page = tree.xpath('//a[contains(@class,"js-next") and not(contains(@class,"disabled"))]/@href')
        next_page_url = urljoin(page_url, next_page[0]) if next_page else None

        return links, next_page_url