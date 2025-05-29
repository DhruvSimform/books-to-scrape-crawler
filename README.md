# Web Scraping Hands-On Task (Day 1 & 2)

## Script Overview

This repository includes a Python script for web scraping, designed to extract data from websites efficiently. The script supports pagination and uses popular libraries for HTTP requests and HTML parsing.

### Features
- Scrapes data from a given URL.
- Handles pagination to scrape multiple pages.
- Extracts book details such as title, price, and availability.
- Saves HTML pages locally for reference.
- Outputs scraped data in JSON format.

### Libraries Used
- **Requests**: For making HTTP requests.
- **BeautifulSoup**: For parsing HTML and extracting data.
- **JSON**: For handling JSON data.
- **Argparse**: For parsing command-line arguments.
- **Datetime**: For timestamping output files.
- **Logger**: For logging events during execution.

### How to Use
1. Run the script with the following command:
    ```bash
    python script.py <base_url> [--prefix <prefix>] [--page <starting_page>] [--suffix <suffix>] [--max_page <max_pages>]
    ```
    - `<base_url>`: The URL to scrape.
    - `--prefix`: Optional prefix for pagination.
    - `--page`: Starting page number (optional).
    - `--suffix`: Optional suffix for pagination.
    - `--max_page`: Maximum number of pages to scrape.

2. Example usage:
    ```bash
    python script.py https://example.com/books --prefix "?page=" --page 1 --max_page 5
    ```

3. Scraped data will be saved in the `scraped_data` folder as a JSON file.

### Notes
- Ensure compliance with the website's `robots.txt` file.
- Avoid sending frequent requests to prevent server overload.

### Output
- Scraped data includes:
  - Book title
  - URL
  - Price
  - Availability
- HTML pages are saved in the `html_pages` folder for debugging purposes.

### Disclaimer
This script is intended for educational purposes only. Use responsibly and adhere to legal and ethical guidelines.

