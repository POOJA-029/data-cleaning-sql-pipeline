"""
Data Cleaning & SQL Pipeline
Author: Pooja
Description: Cleans messy e-commerce order data, loads it into SQLite,
and generates business summaries and a revenue chart.
"""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "sample_messy_orders.csv"
CLEAN_FILE = BASE_DIR / "cleaned_orders.csv"
DB_FILE = BASE_DIR / "orders.db"
CHART_FILE = BASE_DIR / "monthly_revenue.png"

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    # Standardize text fields
    text_cols = ["order_id", "customer_id", "service_category",
                 "project_name", "payment_status", "order_status", "notes"]
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()

    # Normalize blank strings to missing values
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # Parse mixed date formats; invalid or missing dates remain NaT
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce", dayfirst=True, format="mixed"
    )

    # Normalize category/status labels
    category_map = {
        "web development": "Web Development",
        "seo": "SEO",
        "data analytics": "Data Analytics",
        "ui ux design": "UI/UX Design",
        "ui/ux design": "UI/UX Design",
    }
    df["service_category"] = (
        df["service_category"].str.lower().map(category_map).fillna(df["service_category"])
    )
    df["payment_status"] = df["payment_status"].str.title()
    df["order_status"] = df["order_status"].str.title()

    # Convert numeric fields safely
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Preserve data quality issues as flags before filling selected values.
    df["is_flagged"] = (
        df["order_id"].isna()
        | df["customer_id"].isna()
        | df["order_date"].isna()
        | df["service_category"].isna()
        | df["quantity"].isna()
        | df["unit_price"].isna()
    )

    # Remove duplicate order IDs, keeping the first occurrence.
    df = df.drop_duplicates(subset=["order_id"], keep="first")

    # Fill quantity with 1 only where missing; retain a flag for auditability.
    df["quantity"] = df["quantity"].fillna(1)
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)

    # Add month key for monthly reporting.
    df["order_month"] = df["order_date"].dt.strftime("%Y-%m")

    # Store missing-value flags in the database instead of silently discarding them.
    df["quality_issue"] = df.apply(
        lambda r: ", ".join(
            label for label, missing in [
                ("missing_order_id", pd.isna(r["order_id"])),
                ("missing_customer_id", pd.isna(r["customer_id"])),
                ("invalid_or_missing_date", pd.isna(r["order_date"])),
                ("missing_category", pd.isna(r["service_category"])),
                ("missing_unit_price", pd.isna(r["unit_price"])),
            ] if missing
        ),
        axis=1
    )
    return df

def load_to_sqlite(df: pd.DataFrame) -> None:
    # Convert pandas nullable values to SQLite-compatible values.
    db_df = df.copy()
    db_df["order_date"] = db_df["order_date"].dt.strftime("%Y-%m-%d")
    db_df = db_df.astype(object).where(pd.notna(db_df), None)
    with sqlite3.connect(DB_FILE) as conn:
        db_df.to_sql("orders", conn, if_exists="replace", index=False)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_month ON orders(order_month)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_category ON orders(service_category)")

def create_chart(df: pd.DataFrame) -> None:
    monthly = (
        df.dropna(subset=["order_month"])
          .groupby("order_month", as_index=False)["revenue"].sum()
          .sort_values("order_month")
    )
    plt.figure(figsize=(10, 5))
    plt.plot(monthly["order_month"], monthly["revenue"], marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=150)
    plt.close()

def main():
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {RAW_FILE}")
    raw = pd.read_csv(RAW_FILE)
    cleaned = clean_data(raw)
    cleaned.to_csv(CLEAN_FILE, index=False)
    load_to_sqlite(cleaned)
    create_chart(cleaned)

    valid_revenue = cleaned["revenue"].sum(skipna=True)
    flagged_count = int(cleaned["is_flagged"].sum())
    print("Pipeline completed successfully.")
    print(f"Raw rows: {len(raw)}")
    print(f"Cleaned unique orders: {len(cleaned)}")
    print(f"Flagged records: {flagged_count}")
    print(f"Total revenue (available prices): {valid_revenue:,.2f}")
    print(f"SQLite database: {DB_FILE.name}")
    print(f"Chart: {CHART_FILE.name}")

if __name__ == "__main__":
    main()
