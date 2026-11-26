# Book Scraper

A simple web scraper that extracts book data from https://books.toscrape.com/ and saves it to CSV.

## Download and Setup Instructions

**Important:** When downloading this project using GitHub's **Download ZIP** option, Windows may create an outer folder named `Python-web-scraper-main`.

If you see another project folder inside it, open the inner folder to access the actual project files.

## Setup

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python scraper.py
```

## Output

- `books.csv` - 1,000 rows with columns: title, category, price_gbp, rating, stock_count, upc, num_reviews, product_url
- `QUALITY_REPORT.md` - Data quality summary

## Project Structure

```
├── scraper.py           # Main scraper
├── books.csv            # Output data
├── requirements.txt     # Dependencies
└── README.md            # This file
```
