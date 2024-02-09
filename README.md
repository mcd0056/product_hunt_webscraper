# Product Details Scraper

This Python script is designed to scrape product details from Product Hunt for a given category URL and append the scraped data to a JSON file. It utilizes Selenium for web scraping and BeautifulSoup for HTML parsing.

## Requirements

- Python 3.x
- Selenium
- ChromeDriverManager
- BeautifulSoup
- Google Chrome (or any other browser supported by Selenium)

## Installation

1. Clone or download the repository to your local machine.
2. Install the required dependencies using pip:

    ```
    pip install -r requirements.txt
    ```

3. Make sure you have Google Chrome installed on your machine, as the script uses ChromeDriver for browser automation.

## Usage

1. Modify the `product_category_url` variable in the script to the desired Product Hunt category URL you want to scrape.
2. Run the script:

    ```
    python product_scraper.py
    ```

3. The script will scrape the product details from the specified category URL and append them to the `products.json` file.
4. Check the JSON file for the scraped product details.

## File Structure

- `product_scraper.py`: The main Python script for scraping and appending product details.
- `products.json`: JSON file to store the scraped product details.
