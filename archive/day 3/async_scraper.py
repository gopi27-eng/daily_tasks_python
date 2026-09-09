import asyncio
import httpx
from bs4 import BeautifulSoup
from loguru import logger

BASE_URL = "http://quotes.toscrape.com/page/{}/"


async def fetch_page(sem: asyncio.Semaphore, client: httpx.AsyncClient, page: int) -> list[dict]:
    """
    Fetch and parse a single quotes page.
    """
    async with sem:  # enforce concurrency limit
        try:
            url = BASE_URL.format(page)
            response = await client.get(url)
            response.raise_for_status()
            logger.info(f"Fetched page {page} successfully")

            soup = BeautifulSoup(response.text, "html.parser")
            quotes = []

            for item in soup.select("div.quote"):
                text_tag = item.select_one("span.text")
                author_tag = item.select_one("small.author")
                tag_list = [t.get_text(strip=True) for t in item.select("div.tags a.tag")]

                quotes.append(
                    {
                        "text": text_tag.get_text(strip=True) if text_tag else None,
                        "author": author_tag.get_text(strip=True) if author_tag else None,
                        "tags": tag_list,
                        "page": page,
                    }
                )

            return quotes

        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch page {page}: {e}")
            return []


async def main():
    sem = asyncio.Semaphore(3)  # max 3 concurrent requests
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_page(sem, client, page) for page in range(1, 6)]
        results = await asyncio.gather(*tasks)

    # Flatten list of lists
    all_quotes = [quote for page_quotes in results for quote in page_quotes]

    logger.info(
        f"Ingestion complete. Extracted {len(all_quotes)} records across {len(results)} pages."
    )

    # For demonstration, print first few records
    for q in all_quotes[:5]:
        logger.info(q)


if __name__ == "__main__":
    asyncio.run(main())
