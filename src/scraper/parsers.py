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
        h1 = soup.find("h1")
        if h1:
            return clean_text(h1.get_text())
        title_tag = soup.find("a", class_="title")
        if title_tag:
            return clean_text(title_tag.get_text())
    except Exception:
        pass
    return ""


def extract_price(soup):
    try:
        price_tag = soup.find("h4", class_="price")
        if price_tag:
            return clean_price(price_tag.get_text())
        price_tag = soup.find("p", class_="price_color")
        if price_tag:
            return clean_price(price_tag.get_text())
    except Exception:
        pass
    return None


def extract_description(soup):
    try:
        desc_tag = soup.find("p", class_="description")
        if desc_tag:
            return clean_text(desc_tag.get_text())
        caption = soup.find("div", class_="caption")
        if caption:
            for p in caption.find_all("p"):
                if "price" not in p.get("class", []):
                    text = clean_text(p.get_text())
                    if text:
                        return text
    except Exception:
        pass
    return ""


def extract_rating(soup):
    try:
        rating_tag = soup.find(attrs={"data-rating": True})
        if rating_tag:
            return rating_tag.get("data-rating", "")
        rating_div = soup.find("div", class_="ratings")
        if rating_div:
            p_tags = rating_div.find_all("p")
            for p in p_tags:
                text = clean_text(p.get_text())
                if text:
                    return text
    except Exception:
        pass
    return ""


def extract_review_count(soup):
    try:
        review_tag = soup.find("div", class_="ratings")
        if review_tag:
            for p in review_tag.find_all("p"):
                text = clean_text(p.get_text())
                if "review" in text.lower() or text.isdigit():
                    return text
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
        table = soup.find("table", class_="table")
        if table:
            rows = table.find_all("tr")
            specs = []
            for row in rows:
                cells = row.find_all(["th", "td"])
                if len(cells) == 2:
                    key = clean_text(cells[0].get_text())
                    val = clean_text(cells[1].get_text())
                    if key and val:
                        specs.append(f"{key}: {val}")
            if specs:
                return " | ".join(specs)
        spec_list = soup.find("ul", class_="list-unstyled")
        if spec_list:
            items = []
            for li in spec_list.find_all("li"):
                text = clean_text(li.get_text())
                if text:
                    items.append(text)
            return " | ".join(items)
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