import asyncio
import time
import aiohttp
from loguru import logger


urls_to_scrape = [
    "http://quotes.toscrape.com/page/1/",
    "http://quotes.toscrape.com/page/2/",
    "http://quotes.toscrape.com/page/3/",
    "http://quotes.toscrape.com/page/4/",
    "http://quotes.toscrape.com/page/5/"
]


async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                logger.info(f"Successfully fetched {url}")
                text = await response.text()
                return None
    except Exception as e:
        logger.error(f"Exception occurred while fetching {url}: {e}")
        return None
    return text

async def scrape_pages(urls):
    logger.info(f"Starting async scraping of {len(urls)} pages")
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]
        html_pages = await asyncio.gather(*tasks)
        logger.success(f"Scraped {len(html_pages)} pages in {time.time() - start_time:.2f} seconds")
        
asyncio.run(scrape_pages(urls_to_scrape))