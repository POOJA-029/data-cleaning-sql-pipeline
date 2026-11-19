# Data Cleaning & SQL Pipeline

## Overview
This project demonstrates an end-to-end data workflow using Python, Pandas, SQLite, SQL, and Matplotlib. It uses a sample e-commerce orders dataset containing intentional duplicate records, missing values, inconsistent date formats, and inconsistent category/status labels.

## Project files
- `sample_messy_orders.csv` — raw sample input (155 rows, including intentional duplicates).
- `clean_pipeline.py` — cleans the data, creates quality flags, loads it into SQLite, and generates a chart.
- `analysis_queries.sql` — three business queries: monthly revenue, top service categories, and incomplete/flagged records.
- `README.md` — setup and execution instructions.

## Requirements
- Python 3.9+
- pandas
- matplotlib

SQLite is included with Python, so no separate database server is required.

## Setup and run

```bash
# 1. Clone the repository and enter its folder
git clone <your-github-repository-url>
cd data-cleaning-sql-pipeline

# 2. Install dependencies
python -m pip install pandas matplotlib

# 3. Run the pipeline
python clean_pipeline.py
```

The script creates:
- `cleaned_orders.csv` — standardized, deduplicated output.
- `orders.db` — SQLite database with an `orders` table.
- `monthly_revenue.png` — monthly revenue chart.

## Run the SQL queries

Open `orders.db` using DB Browser for SQLite, SQLiteStudio, or the `sqlite3` command-line tool, then run the statements in `analysis_queries.sql`.

Example using the SQLite command line:

```bash
sqlite3 orders.db
.read analysis_queries.sql
```

## Cleaning decisions
1. Column names and text values are trimmed and normalized.
2. Blank strings are treated as missing values.
3. Mixed date formats are parsed into a consistent date type; invalid dates become NULL.
4. Service categories and status labels are standardized.
5. Duplicate `order_id` values are removed, keeping the first occurrence.
6. Missing quantity is filled with 1 as a documented assumption. Missing unit prices and key identifiers are not fabricated.
7. `is_flagged` and `quality_issue` preserve visibility of incomplete records.
8. Revenue is calculated as `quantity * unit_price`; records without a valid price have NULL revenue.

## Notes
This is a synthetic dataset created for demonstration purposes. Revenue totals include only rows with a valid calculated revenue. In a production pipeline, business owners should confirm assumptions such as default quantity and duplicate-resolution rules before deployment.
