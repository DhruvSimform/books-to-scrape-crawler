import argparse
import datetime
import json
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
    :type pagination: dict, optional

    :raises requests.exceptions.RequestException: If a request fails
    :raises Exception: For other exceptions during scraping

    :return: Scraped data
    :rtype: dict
    """
    data = {}

    current_page = pagination["page"] if pagination else None
    max_page = pagination["max_page"] if pagination else 1
    prefix = pagination["prefix"] if pagination else ""
    suffix = pagination["suffix"] if pagination else ""

    while current_page is None or current_page <= max_page:
        if pagination:
            url = f"{base_url}{prefix}{current_page}{suffix}"
        else:
            url = base_url

        logger.info(f"Scraping URL: {url}")

        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL: {e}")
            break  # Stop retrying on error

        with open(
            f"html_pages/page_{current_page or 1}.html", "w", encoding="utf-8"
        ) as f:
            f.write(response.text)
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")
        logger.info(f"Found {len(books)} books on page {current_page or 1}")

        for book in books:
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
            break  # If there's no pagination, scrape only once

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

    pagination = None
    if args.page is not None:
        pagination = {
            "prefix": args.prefix,
            "page": args.page,
            "suffix": args.suffix,
            "max_page": args.max_page,
        }

    try:
        scraped_data = scraping(args.url, pagination)
        print(json.dumps(scraped_data, indent=4, ensure_ascii=False))

        with open(
            f"scraped_data/scraped_data_{datetime.datetime.now()}.json",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(json.dumps(scraped_data, indent=4, ensure_ascii=False))
        logger.info("Scraping completed successfully.")

    except requests.exceptions.RequestException as re:
        logger.error(f"RequestException: {re}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
