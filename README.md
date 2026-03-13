# Catalog Scraper Mini Project

This is my Quiz 1 project for Tools & Technologies for Data Science. The goal was to build a web scraper that goes through an e-commerce test site, collects product data from all categories and pages, and saves it into CSV files.

## What This Project Does

The scraper visits this website:
https://webscraper.io/test-sites/e-commerce/static

It automatically finds all categories, goes into each subcategory , goes through every page, opens each product page individually, and collects the data. At the end it saves everything into two CSV files.

## Tools Used

- Python
- uv (for managing the project and packages)
- requests (for fetching web pages)
- beautifulsoup4 (for reading and extracting HTML)
- pandas (for saving data to CSV)
- Git and GitHub 

## How I Set Up the Project

I used uv to initialize and manage the whole project:
```bash
uv init catalog-scraper
cd catalog-scraper
uv add requests beautifulsoup4 pandas
```

## How to Install and Run

First install the dependencies:
```bash
uv sync
```

Then run the scraper:
```bash
uv run python src/main.py
```

To run the tests:
```bash
uv run python tests/test_utils.py
```

## Branch Workflow I Followed

I followed the required branching workflow step by step:

1. Created the repository with `main`
2. Created `dev` branch from main
3. Created `feature/catalog-navigation` 
4. Created `feature/product-details` 
5. Merged both feature branches into `dev`
6. Created `fix/url-resolution` 
7. Created `fix/deduplication` 
8. Merged both fix branches into `dev`
9. After testing, merged `dev` into `main`

## Results

- 147 products scraped in total
- 20 pages crawled for Laptops alone
- 3 subcategories covered: Laptops, Tablets, Touch
- 0 duplicates found

## Output Files

- `data/products.csv` — contains all 147 products with category, subcategory, title, price, URL, description, rating, and more
- `data/category_summary.csv` — contains average, min and max prices per subcategory along with missing description counts

## Assumptions

- Since the target website is a static site, I used requests and BeautifulSoup which is enough without needing JavaScript rendering tools
- I used the product URL to identify and remove duplicates

## Limitations

- If the website structure changes, the CSS selectors in the code may need to be updated
- No delay between requests since this is a test site made for scraping practice