# Web Scraping Hands-On Task (Day 1 & 2)

## Overview

This repository contains Python scripts for web scraping, designed to extract book data efficiently from websites. The scripts demonstrate synchronous and asynchronous scraping techniques, handle pagination, and save the extracted data in JSON format.

## Features

- **Synchronous and Asynchronous Scraping**: Compare performance between sequential and parallel scraping methods.
- **Pagination Handling**: Scrape multiple pages seamlessly.
- **Data Extraction**: Extract book details such as title, price, availability, and rating.
- **HTML Storage**: Save HTML pages locally for debugging and reference.
- **JSON Output**: Store scraped data in structured JSON files.

## Libraries Used

- **Requests**: For synchronous HTTP requests.
- **Aiohttp**: For asynchronous HTTP requests.
- **BeautifulSoup**: For HTML parsing and data extraction.
- **JSON**: For handling and storing scraped data.
- **Argparse**: For parsing command-line arguments.
- **Datetime**: For timestamping output files.
- **Multiprocessing**: For parallel data parsing.
- **Logger**: For logging events during execution.

## How to Use

### Synchronous Scraping
Run the `sync_fetch.py` script to scrape data sequentially:
```bash
python sync_fetch.py
```
The scraped data will be saved in the `scraped_data/books_sync.json` file.

### Asynchronous Scraping
Run the `pagination_scrap.py` script to scrape data asynchronously:
```bash
python pagination_scrap.py
```
The scraped data will be saved in the `scraped_data/books.json` file.

### Custom Scraping with Pagination
Run the `main.py` script with optional pagination settings:
```bash
python main.py <base_url> [--prefix <prefix>] [--page <starting_page>] [--suffix <suffix>] [--max_page <max_pages>]
```
Example:
```bash
python main.py https://books.toscrape.com/catalogue/ --prefix "page-" --page 1 --max_page 50
```
The scraped data will be saved in the `scraped_data` folder with a timestamped filename.

### Synchronous vs Asynchronous Comparison
Run the `main1.py` script to compare synchronous and asynchronous scraping performance:
```bash
python main1.py
```

## Output

- **Scraped Data**: Includes book title, URL, price, availability, and rating.
- **HTML Pages**: Saved in the `html_pages` folder for debugging purposes.
- **JSON Files**: Stored in the `scraped_data` folder.

## Notes

- Ensure compliance with the website's `robots.txt` file.
- Avoid sending frequent requests to prevent server overload.
- Use responsibly and adhere to legal and ethical guidelines.

## Disclaimer

This project is intended for educational purposes only. Ensure you have permission to scrape the target website and comply with all applicable laws and regulations.
