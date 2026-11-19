# Data Cleaning & SQL Pipeline

## Overview
This project demonstrates an end-to-end data workflow using Python, Pandas, SQLite, SQL, and Matplotlib. It uses a sample e-commerce orders dataset containing duplicate records, missing values, inconsistent date formats, and inconsistent category/status labels.

## Project Files
- `sample_messy_orders.csv` – Raw sample dataset.
- `clean_pipeline.py` – Python data cleaning and database loading script.
- `analysis_queries.sql` – Three SQL business queries.
- `cleaned_orders.csv` – Cleaned dataset.
- `orders.db` – SQLite database.
- `monthly_revenue.png` – Monthly revenue chart.
- `RUN_SUMMARY.md` – Execution summary.

## Requirements
- Python 3.9+
- Pandas
- Matplotlib
- SQLite

## Setup and Run

### 1. Clone the repository

```bash
git clone https://github.com/POOJA-029/data-cleaning-sql-pipeline.git
cd data-cleaning-sql-pipeline
```

### 2. Install dependencies

```bash
python -m pip install pandas matplotlib
```

### 3. Run the pipeline

```bash
python clean_pipeline.py
```

## SQL Queries

Open `orders.db` using DB Browser for SQLite or SQLiteStudio and execute the queries from `analysis_queries.sql`.

## Cleaning Process

1. Removed duplicate order IDs.
2. Handled missing values.
3. Standardized date formats.
4. Cleaned category and status labels.
5. Identified incomplete records using quality flags.
6. Loaded cleaned data into SQLite.
7. Generated monthly revenue insights and a chart.

## Notes
This project uses a synthetic e-commerce dataset created for demonstration purposes.
