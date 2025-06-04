"""
Web scraper for book data using BeautifulSoup with optional pagination.
"""

import argparse
import datetime
import json
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from logger import logger



def scraping(base_url, pagination=None):
    """
    Scrapes the provided URL, handling optional pagination.

    :param base_url: Base URL to scrape
    :type base_url: str
    :param pagination: Pagination settings, defaults to None
    :type pagination: dict, optionalNNN
    :return: Scraped data
    :rtype: dict
    """
    data = {}

    current_page = pagination["page"] if pagination else 1
    max_page = pagination["max_page"] if pagination else 1
    prefix = pagination["prefix"] if pagination else ""
    suffix = pagination["suffix"] if pagination else ""

    while current_page <= max_page:
        url = f"{base_url}{prefix}{current_page}{suffix}" if pagination else base_url

        logger.info("Scraping URL: %s", url)

        try:
            response = requests.get(url, timeout=10)
            response.encoding = "utf-8"
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching URL: %s", e)
            break

        os.makedirs("html_pages", exist_ok=True)
        with open(
            f"html_pages/page_{current_page}.html", "w", encoding="utf-8"
        ) as html_file:
            html_file.write(response.text)

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        logger.info("Found %d books on page %d", len(books), current_page)

        for book in books:
            # pylint: disable=no-member
            book_title = book.h3.a["title"]
            book_url = urljoin(base_url, book.h3.a["href"])
            book_price = book.find("p", class_="price_color").text
            book_availability = book.find(
                "p", class_="instock availability"
            ).text.strip()

            data[book_title] = {
                "url": book_url,
                "price": book_price,
                "availability": book_availability,
            }

        if not pagination:
            break

        current_page += 1

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape book data from a website.")
    parser.add_argument("url", type=str, help="Base URL to scrape")
    parser.add_argument("--prefix", type=str, default="", help="Pagination prefix")
    parser.add_argument("--page", type=int, default=None, help="Starting page number")
    parser.add_argument("--suffix", type=str, default="", help="Pagination suffix")
    parser.add_argument(
        "--max_page", type=int, default=1, help="Maximum number of pages to scrape"
    )

    args = parser.parse_args()

    PAGINATION_ARGS = None
    if args.page is not None:
        PAGINATION_ARGS = {
            "prefix": args.prefix,
            "page": args.page,
            "suffix": args.suffix,
            "max_page": args.max_page,
        }

    try:
        scraped_data = scraping(args.url, PAGINATION_ARGS)
        print(json.dumps(scraped_data, indent=4, ensure_ascii=False))

        os.makedirs("scraped_data", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        FILENAME = f"scraped_data/scraped_data_{timestamp}.json"
        with open(FILENAME, "w", encoding="utf-8") as json_file:
            json.dump(scraped_data, json_file, indent=4, ensure_ascii=False)

        logger.info("Scraping completed successfully.")
    except requests.exceptions.RequestException as re:
        logger.error("RequestException: %s", re)
