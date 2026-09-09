import sys
import httpx
from loguru import logger


def check_api_health(url:str):
    logger.info(f"---checking the api status---")
    
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            logger.info(f"Successfully connected:{url}")
            sys.exit(0)
        else:
            logger.error(f"API return status {response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Network failuer: {e}")
        
    logger.warning("This line should never print if sys.exit() works correctly.")
    sys.exit(1)

if __name__ == "__main__":
    check_api_health("https://httpbin.org/status/200")
