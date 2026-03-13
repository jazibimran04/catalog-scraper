import requests
from urllib.parse import urljoin

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def safe_get(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"  [WARN] Attempt {attempt+1} failed for {url}: {e}")
    print(f"  [ERROR] Could not fetch: {url}")
    return None

def resolve_url(relative_url, base=BASE_URL):
    if not relative_url:
        return None
    if relative_url.startswith("http"):
        return relative_url
    return urljoin(base, relative_url)

def clean_text(text):
    if text is None:
        return ""
    return " ".join(text.strip().split())

def clean_price(price_text):
    if not price_text:
        return None
    try:
        cleaned = price_text.strip().replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return None

def deduplicate(products):
    """
    Fix: removes duplicate products by URL.
    Also tracks how many were removed per subcategory.
    """
    seen_urls = set()
    unique = []
    duplicates_removed = 0

    for product in products:
        url = product.get("product_url", "").strip().rstrip("/")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(product)
        elif url:
            duplicates_removed += 1
            print(f"  [DEDUP] Duplicate removed: {url}")

    return unique, duplicates_removed