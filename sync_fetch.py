import requests
from bs4 import BeautifulSoup
import time
import json
import os

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGES = 50


def fetch_html(url: str) -> str:
    """Fetch HTML content using requests."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def parse_books(html: str) -> list[dict]:
    """Parse book data from HTML."""
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


def main():
    all_books = []
    start_time = time.time()

    for i in range(1, TOTAL_PAGES + 1):
        url = BASE_URL.format(i)
        html = fetch_html(url)
        books = parse_books(html)
        all_books.extend(books)

    end_time = time.time()

    os.makedirs("scraped_data", exist_ok=True)
    with open("scraped_data/books_sync.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=4, ensure_ascii=False)

    print(f"✅ Scraped {len(all_books)} books.")
    print(f"⏱️  Time taken (sequential): {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
