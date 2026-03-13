from bs4 import BeautifulSoup
from .utils import safe_get, resolve_url, BASE_URL


def get_soup(url):
    response = safe_get(url)
    if response is None:
        return None
    return BeautifulSoup(response.text, "html.parser")


def discover_categories(base_url=BASE_URL):
    print(f"[CRAWLER] Discovering categories from: {base_url}")
    soup = get_soup(base_url)
    if not soup:
        return []

    categories = []

    # Categories are inside <ul class="nav flex-column">
    nav = soup.find("ul", class_="flex-column")
    if not nav:
        print("  [WARN] Could not find category nav.")
        return []

    for a in nav.find_all("a", href=True):
        href = a.get("href", "")
        name = a.get_text(strip=True)
        # Only grab top-level category links (computers, phones)
        if "e-commerce/static" in href and href != "/test-sites/e-commerce/static":
            url = resolve_url(href)
            if url and name:
                categories.append({"name": name, "url": url})

    print(f"  [CRAWLER] Found {len(categories)} categories.")
    return categories


def discover_subcategories(category):
    cat_name = category["name"]
    cat_url = category["url"]

    print(f"  [CRAWLER] Looking for subcategories in: {cat_name}")
    soup = get_soup(cat_url)
    if not soup:
        return [{"name": cat_name, "url": cat_url, "category": cat_name}]

    subcategories = []

    # Subcategories are also in <ul class="nav flex-column"> on the category page
    nav = soup.find("ul", class_="flex-column")
    if nav:
        for a in nav.find_all("a", href=True):
            href = a.get("href", "")
            sub_name = a.get_text(strip=True)
            # Subcategory links go deeper than the category
            if "e-commerce/static" in href and cat_name.lower() in href.lower():
                sub_url = resolve_url(href)
                if sub_url and sub_name and sub_url != cat_url:
                    subcategories.append({
                        "name": sub_name,
                        "url": sub_url,
                        "category": cat_name
                    })

    if not subcategories:
        subcategories = [{"name": cat_name, "url": cat_url, "category": cat_name}]

    print(f"    [CRAWLER] Found {len(subcategories)} subcategories for '{cat_name}'.")
    return subcategories


def get_next_page_url(soup):
    pagination = soup.find("ul", class_="pagination")
    if not pagination:
        return None
    for li in pagination.find_all("li"):
        a = li.find("a")
        if not a:
            continue
        text = a.get_text(strip=True)
        if "›" in text or "»" in text or text.lower() == "next":
            href = a.get("href", "")
            if href:
                return resolve_url(href)
    return None


def crawl_subcategory(subcategory):
    sub_name = subcategory["name"]
    sub_url = subcategory["url"]
    cat_name = subcategory["category"]

    print(f"    [CRAWLER] Crawling subcategory: {sub_name}")
    all_product_links = []
    current_url = sub_url
    page_num = 1

    while current_url:
        print(f"      [CRAWLER] Page {page_num}: {current_url}")
        soup = get_soup(current_url)
        if not soup:
            break

        thumbnails = soup.find_all("div", class_="thumbnail")
        for thumb in thumbnails:
            a_tag = thumb.find("a", class_="title")
            if not a_tag:
                a_tag = thumb.find("a")
            if not a_tag:
                continue
            href = a_tag.get("href", "")
            url = resolve_url(href)
            if url:
                all_product_links.append({
                    "url": url,
                    "category": cat_name,
                    "subcategory": sub_name,
                    "page": page_num
                })

        print(f"        Found {len(thumbnails)} products on page {page_num}.")
        next_url = get_next_page_url(soup)
        if next_url and next_url != current_url:
            current_url = next_url
            page_num += 1
        else:
            break

    print(f"    [CRAWLER] Total products in '{sub_name}': {len(all_product_links)}")
    return all_product_links


def run_crawler():
    print("\n" + "="*60)
    print("STEP 1: Starting catalog crawler")
    print("="*60)

    categories = discover_categories()
    all_product_links = []

    for category in categories:
        subcategories = discover_subcategories(category)
        for subcategory in subcategories:
            links = crawl_subcategory(subcategory)
            all_product_links.extend(links)

    print(f"\n[CRAWLER] Done. Total product links: {len(all_product_links)}")
    return all_product_links