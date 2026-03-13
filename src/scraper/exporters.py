import os
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_products_csv(products):
    ensure_output_dir()
    if not products:
        print("[EXPORTER] No products to export.")
        return

    df = pd.DataFrame(products)

    required_columns = [
        "category", "subcategory", "product_title", "price",
        "product_url", "image_url", "description", "rating",
        "review_count", "spec", "page_number"
    ]
    for col in required_columns:
        if col not in df.columns:
            df[col] = ""

    df = df[required_columns]
    output_path = os.path.join(OUTPUT_DIR, "products.csv")
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[EXPORTER] products.csv saved → {output_path} ({len(df)} rows)")
    return df

def export_category_summary_csv(products, duplicates_removed_map=None):
    ensure_output_dir()
    if not products:
        print("[EXPORTER] No products to summarize.")
        return

    df = pd.DataFrame(products)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["has_description"] = df["description"].apply(
        lambda x: 0 if (x is None or str(x).strip() == "") else 1
    )

    summary = df.groupby(["category", "subcategory"]).agg(
        total_products=("product_url", "count"),
        average_price=("price", "mean"),
        min_price=("price", "min"),
        max_price=("price", "max"),
        missing_descriptions=("has_description", lambda x: (x == 0).sum())
    ).reset_index()

    summary["average_price"] = summary["average_price"].round(2)

    if duplicates_removed_map:
        summary["duplicates_removed"] = summary["subcategory"].map(
            lambda s: duplicates_removed_map.get(s, 0)
        )
    else:
        summary["duplicates_removed"] = 0

    output_path = os.path.join(OUTPUT_DIR, "category_summary.csv")
    summary.to_csv(output_path, index=False, encoding="utf-8")
    print(f"[EXPORTER] category_summary.csv saved → {output_path} ({len(summary)} rows)")
    print("\n[EXPORTER] Summary Preview:")
    print(summary.to_string(index=False))
    return summary

def export_all(products, duplicates_removed_map=None):
    print("\n" + "="*60)
    print("STEP 4: Exporting CSV files")
    print("="*60)
    export_products_csv(products)
    export_category_summary_csv(products, duplicates_removed_map)
    print("\n[EXPORTER] All files exported to /data folder.")