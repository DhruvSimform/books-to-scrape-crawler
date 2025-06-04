import asyncio
import aiohttp
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count
from typing import List, Dict


BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGES = 50


async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    """Asynchronously fetch HTML content from a URL."""
    async with session.get(url, timeout=15) as response:
        return await response.text()


async def download_all_pages() -> List[str]:
    """Download all book pages asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, BASE_URL.format(i)) for i in range(1, TOTAL_PAGES + 1)]
        return await asyncio.gather(*tasks)


def parse_books(html: str) -> List[Dict]:
    """Parse HTML and extract book details."""
    soup = BeautifulSoup(html, "lxml")
    books = []

    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = article.select_one(".price_color").text.strip()
        availability = article.select_one(".instock.availability").text.strip()
        rating_class = article.select_one("p.star-rating")["class"]
        rating = next((r for r in rating_class if r != "star-rating"), "Unrated")

        books.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating
        })

    return books


def parallel_parse(html_pages: List[str]) -> List[Dict]:
    """Parse all HTML pages in parallel using multiprocessing."""
    with Pool(cpu_count()) as pool:
        results = pool.map(parse_books, html_pages)

    # Flatten list of lists
    return [book for sublist in results for book in sublist]


if __name__ == "__main__":
    import time
    import json
    import os

    start = time.time()
    html_pages = asyncio.run(download_all_pages())
    print(f"Downloaded {len(html_pages)} pages in {time.time() - start:.2f}s")

    start = time.time()
    all_books = parallel_parse(html_pages)
    print(f"Parsed {len(all_books)} books in {time.time() - start:.2f}s")

    # Save result
    os.makedirs("scraped_data", exist_ok=True)
    with open("scraped_data/books.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=4, ensure_ascii=False)

    print("✅ Scraping complete.")
