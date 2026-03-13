from bs4 import BeautifulSoup
from .utils import safe_get, resolve_url, clean_text, clean_price


def parse_product_detail(link_info):
    url = link_info["url"]
    category = link_info["category"]
    subcategory = link_info["subcategory"]
    page = link_info["page"]

    response = safe_get(url)
    if not response:
        print(f"    [PARSER] Skipping (failed to load): {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title = extract_title(soup)
    price = extract_price(soup)
    description = extract_description(soup)
    rating = extract_rating(soup)
    review_count = extract_review_count(soup)
    image_url = extract_image_url(soup, url)
    spec = extract_spec(soup)

    return {
        "category": category,
        "subcategory": subcategory,
        "product_title": title,
        "price": price,
        "product_url": url,
        "image_url": image_url,
        "description": description,
        "rating": rating,
        "review_count": review_count,
        "spec": spec,
        "page_number": page
    }


def extract_title(soup):
    try:
        tag = soup.find("h4", class_="title")
        if tag:
            return clean_text(tag.get_text())
    except Exception:
        pass
    return ""


def extract_price(soup):
    try:
        tag = soup.find("h4", class_="price")
        if tag:
            return clean_price(tag.get_text())
    except Exception:
        pass
    return None


def extract_description(soup):
    try:
        tag = soup.find("p", class_="description")
        if tag:
            return clean_text(tag.get_text())
    except Exception:
        pass
    return ""


def extract_rating(soup):
    try:
        tag = soup.find("p", class_="review-count")
        if tag:
            return clean_text(tag.get_text())
    except Exception:
        pass
    return ""


def extract_review_count(soup):
    try:
        tag = soup.find("p", class_="review-count")
        if tag:
            span = tag.find("span", itemprop="reviewCount")
            if span:
                return clean_text(span.get_text())
    except Exception:
        pass
    return ""


def extract_image_url(soup, product_url):
    try:
        img_tag = soup.find("img", class_="img-responsive")
        if img_tag:
            src = img_tag.get("src", "")
            return resolve_url(src, product_url)
        img_tag = soup.find("img")
        if img_tag:
            src = img_tag.get("src", "")
            return resolve_url(src, product_url)
    except Exception:
        pass
    return ""


def extract_spec(soup):
    try:
        tag = soup.find("p", class_="description")
        if tag:
            return clean_text(tag.get_text())
    except Exception:
        pass
    return ""


def parse_all_products(product_links):
    print("\n" + "="*60)
    print("STEP 2: Parsing product detail pages")
    print("="*60)

    products = []
    total = len(product_links)

    for i, link_info in enumerate(product_links, 1):
        print(f"  [PARSER] ({i}/{total}) {link_info['url']}")
        product = parse_product_detail(link_info)
        if product:
            products.append(product)

    print(f"\n[PARSER] Done. Successfully parsed {len(products)} products.")
    return products