import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scraper.utils import clean_price, clean_text, resolve_url, deduplicate


def test_clean_price():
    assert clean_price("$295.99") == 295.99
    assert clean_price("$11.50") == 11.50
    assert clean_price(None) is None
    assert clean_price("") is None
    assert clean_price("abc") is None
    print("✓ test_clean_price passed")


def test_clean_text():
    assert clean_text("  hello  world  ") == "hello world"
    assert clean_text(None) == ""
    assert clean_text("") == ""
    print("✓ test_clean_text passed")


def test_resolve_url():
    base = "https://webscraper.io/test-sites/e-commerce/static"
    result = resolve_url("/test-sites/e-commerce/static/computers", base)
    assert result.startswith("https://webscraper.io")
    assert "computers" in result
    print("✓ test_resolve_url passed")


def test_deduplicate():
    products = [
        {"product_url": "https://example.com/product/1", "name": "A"},
        {"product_url": "https://example.com/product/2", "name": "B"},
        {"product_url": "https://example.com/product/1", "name": "A duplicate"},
    ]
    unique, removed = deduplicate(products)
    assert len(unique) == 2
    assert removed == 1
    print("✓ test_deduplicate passed")


if __name__ == "__main__":
    test_clean_price()
    test_clean_text()
    test_resolve_url()
    test_deduplicate()
    print("\n✅ All tests passed!")