"""
Web Scraper for book data with sync vs async parallel calls,
demonstrating time differences.
"""

import time
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup

URLS = [
    "https://httpbin.org/delay/3",
    "https://httpbin.org/delay/3",
    "https://httpbin.org/delay/3",
    "https://httpbin.org/delay/3",
    "https://httpbin.org/delay/3",

]


def sync_scrape(urls):
    """
    Scrape a list of URLs synchronously using requests.

    :param urls: List of URLs to fetch.
    :type urls: list[str]
    :return: List of response texts.
    :rtype: list[str]
    """
    results = []
    for url in urls:
        r = requests.get(url, timeout=10)
        results.append(r.text)
    return results


async def async_scrape(urls):
    """
    Scrape a list of URLs in parallel using aiohttp.

    :param urls: List of URLs to fetch.
    :type urls: list[str]
    :return: List of response texts.
    :rtype: list[str]
    """
    async def fetch(session, url):
        async with session.get(url, timeout=10) as resp:
            return await resp.text()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, u) for u in urls]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Synchronous run
    start_sync = time.perf_counter()
    sync_results = sync_scrape(URLS)
    duration_sync = time.perf_counter() - start_sync
    print(f"Synchronous fetch took {duration_sync:.2f} seconds")

    # Asynchronous run
    start_async = time.perf_counter()
    async_results = asyncio.run(async_scrape(URLS))
    duration_async = time.perf_counter() - start_async
    print(f"Asynchronous fetch took {duration_async:.2f} seconds")

    # Verify lengths
    for i, (s, a) in enumerate(zip(sync_results, async_results), 1):
        print(f"URL {i} → sync len={len(s)}, async len={len(a)}")
