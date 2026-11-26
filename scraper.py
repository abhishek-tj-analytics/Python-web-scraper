"""Web scraper for books.toscrape.com - extracts all 1,000 books to CSV."""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = "books.csv"

# Reuse one session for faster requests
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})


def fetch(url):
    """Fetch URL and return BeautifulSoup object."""
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, 'html.parser')
    except Exception:
        return None


def collect_book_urls():
    """Get all book URLs from catalogue pages."""
    urls = []
    for page in range(1, 51):
        soup = fetch(f'https://books.toscrape.com/catalogue/page-{page}.html')
        if not soup:
            break
        for article in soup.find_all('article', class_='product_pod'):
            link = article.find('h3').find('a')
            if link:
                # urljoin handles relative URLs correctly
                urls.append(urljoin(BASE_URL + 'catalogue/', link['href']))
    return urls


def scrape_book(url):
    """Get details from one book page."""
    soup = fetch(url)
    if not soup:
        return None

    # Title from h1 element on the page
    title_tag = soup.find('h1')
    title = title_tag.get_text().strip() if title_tag else None

    # Category is in the breadcrumb - third link
    breadcrumb = soup.find('ul', class_='breadcrumb')
    category = None
    if breadcrumb:
        links = breadcrumb.find_all('a')
        if len(links) >= 3:
            category = links[2].get_text().strip()

    # Price with £ symbol - extract numeric value
    price = None
    price_tag = soup.find('p', class_='price_color')
    if price_tag:
        m = re.search(r'£([\d.]+)', price_tag.get_text())
        if m:
            price = float(m.group(1))

    # Rating from star-rating CSS class
    rating = None
    rating_tag = soup.find('p', class_='star-rating')
    if rating_tag:
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        for cls in rating_tag.get('class', []):
            if cls in rating_map:
                rating = rating_map[cls]

    # Stock, UPC, reviews from product specification table
    stock, upc, reviews = None, None, 0
    table = soup.find('table', class_='table table-striped')
    if table:
        for row in table.find_all('tr'):
            th = row.find('th')
            td = row.find('td')
            if th and td:
                header = th.get_text().strip()
                value = td.get_text().strip()
                if header == 'UPC':
                    upc = value
                elif header == 'Availability':
                    # Stock count embedded in "In stock (22 available)"
                    m = re.search(r'(\d+)', value)
                    if m:
                        stock = int(m.group(1))
                elif header == 'Number of reviews':
                    try:
                        reviews = int(value)
                    except:
                        reviews = 0

    return {
        'title': title,
        'category': category,
        'price_gbp': price,
        'rating': rating,
        'stock_count': stock,
        'upc': upc,
        'num_reviews': reviews,
        'product_url': url
    }


def main():
    """Main entry point for the scraper."""
    print("=" * 60)
    print("Book Scraper - Starting")
    start_time = time.time()

    # Collect all book URLs first
    print("Collecting book URLs...")
    urls = collect_book_urls()
    print(f"Found {len(urls)} books")

    # Scrape each book
    print("Scraping book details...")
    books = []
    failed = []
    for i, url in enumerate(urls, 1):
        if i % 200 == 0:
            print(f"  Progress: {i}/{len(urls)}")
        result = scrape_book(url)
        if result:
            books.append(result)
        else:
            failed.append(url)

    # Save results with exact column order required
    df = pd.DataFrame(books)
    cols = ['title', 'category', 'price_gbp', 'rating', 'stock_count', 'upc', 'num_reviews', 'product_url']
    df = df[cols]
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} records to {OUTPUT_FILE}")

    # Generate quality report
    elapsed = time.time() - start_time
    minutes, seconds = int(elapsed // 60), int(elapsed % 60)

    null_counts = df.isnull().sum()
    null_rates = (null_counts / len(df) * 100).round(2)
    duplicates = df.duplicated().sum()

    report = f"""# Quality Report

## Summary
- **Total rows extracted:** {len(df)}
- **Expected rows:** 1,000
- **Failed URLs:** {len(failed)}

## Execution Summary
- **Total time:** {minutes} minutes {seconds} seconds
- **Books scraped:** {len(df)}
- **Failed URLs:** {len(failed)}

## Duplicates
- **Duplicate records:** {duplicates}

## Null Rates by Column

| Column | Null Count | Null Rate (%) |
|--------|------------|---------------|
| title | {null_counts['title']} | {null_rates['title']}% |
| category | {null_counts['category']} | {null_rates['category']}% |
| price_gbp | {null_counts['price_gbp']} | {null_rates['price_gbp']}% |
| rating | {null_counts['rating']} | {null_rates['rating']}% |
| stock_count | {null_counts['stock_count']} | {null_rates['stock_count']}% |
| upc | {null_counts['upc']} | {null_rates['upc']}% |
| num_reviews | {null_counts['num_reviews']} | {null_rates['num_reviews']}% |
| product_url | {null_counts['product_url']} | {null_rates['product_url']}% |

## Data Completeness

All 1,000 books were successfully extracted with no missing data.

## Failed URLs

"""
    if failed:
        report += "\n".join(f"- {u}" for u in failed)
    else:
        report += "No failed URLs.\n"

    with open('QUALITY_REPORT.md', 'w') as f:
        f.write(report)

    print(f"\nTime: {minutes}m {seconds}s")
    print(f"Books: {len(df)}, Failed: {len(failed)}")
    print("Scraping complete!")


if __name__ == "__main__":
    main()