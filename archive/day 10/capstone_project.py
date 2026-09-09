import os
import asyncio
import aiohttp
import polars as pl
from dotenv import load_dotenv
from tqdm.asyncio import tqdm
from logging_utils.log import setup_logger

logger = setup_logger("async_pipeline.log")


# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("QUIKJET_API_TOKEN", "default_token")

async def fetch_hub_data(session, hub_code):
    """Hits a mock API endpoint to get data for a specific hub."""
    url = f"https://httpbin.org/anything?hub={hub_code}&token={API_TOKEN}"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                logger.error(f"Bad status {response.status} for {hub_code}")
                return None
    except Exception as e:
        logger.error(f"Failed to fetch {hub_code}: {e}")
        return None

async def main():
    logger.info("Booting the async ingestion engine...")
    hub_codes = [f"HUB_{i}" for i in range(100)]
    logger.info(f"Preparing to fetch data from {len(hub_codes)} concurrently...")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_hub_data(session, hub) for hub in hub_codes]
        results = await tqdm.gather(*tasks, desc="Fetch Hub API")

    logger.info("API ingestion completed → Building Polars DataFrame...")
    valid_results = [r for r in results if r is not None]
    raw_data = [res["args"] for res in valid_results]

    pl_df = pl.DataFrame(raw_data)
    print(pl_df.head())
    logger.info("Successfully converted raw_data to Polars DataFrame!")

if __name__ == "__main__":
    asyncio.run(main())
