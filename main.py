# main.py
"""
Data Analytics Project
- Loads a dataset, performs cleaning, summary statistics, a simple aggregation,
  and saves a short CSV report.
Run: python main.py
"""

# Core libs
import os
import pandas as pd          # pandas is used for loading and manipulating tabular data
import numpy as np
import matplotlib.pyplot as plt

# **CHANGE**: set paths/names to match your repo or dataset
DATA_DIR = "data"
RAW_CSV = os.path.join(DATA_DIR, "sample_sales.csv")   # sample path
REPORT_CSV = os.path.join(DATA_DIR, "sales_summary_report.csv")
PLOT_PNG = os.path.join(DATA_DIR, "sales_over_time.png")

def generate_sample_data(path):
    """Generates a small sample sales dataset so the project runs without external files."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rng = np.random.default_rng(42)
    dates = pd.date_range("2024-01-01", periods=120, freq="D")
    df = pd.DataFrame({
        "date": np.tile(dates, 1),
        "region": rng.choice(["North","South","East","West"], size=len(dates)),
        "product": rng.choice(["Widget A","Widget B","Widget C"], size=len(dates)),
        "units_sold": rng.integers(1, 25, size=len(dates)),
        "unit_price": rng.choice([9.99, 14.99, 19.99], size=len(dates))
    })
    df["revenue"] = df["units_sold"] * df["unit_price"]
    df.to_csv(path, index=False)
    print(f"Generated sample data at {path}")

def load_data(path):
    """Load CSV into a pandas DataFrame."""
    if not os.path.exists(path):
        generate_sample_data(path)
    df = pd.read_csv(path, parse_dates=["date"])
    return df

def clean_data(df):
    """Basic cleaning: drop duplicates, fill missing values (simple)."""
    # **CHANGE**: adjust cleaning rules to match your real dataset and domain knowledge
    df = df.drop_duplicates()
    df["units_sold"] = df["units_sold"].fillna(0).astype(int)
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())
    df["revenue"] = df["units_sold"] * df["unit_price"]
    return df

def summary_statistics(df):
    """Produce summary stats and aggregated metrics by month and product."""
    df["month"] = df["date"].dt.to_period("M")
    overall = df[["units_sold","revenue"]].agg(["sum","mean","median"]).T.rename(columns={
        "sum":"total", "mean":"avg", "median":"median"
    })
    by_product = df.groupby("product").agg({
        "units_sold":"sum",
        "revenue":"sum"
    }).sort_values("revenue", ascending=False)
    by_month = df.groupby("month").agg({"revenue":"sum"}).reset_index()
    return overall, by_product, by_month

def save_report(overall, by_product, report_path):
    """Save a concise CSV report that recruiters can open quickly."""
    # **CHANGE**: adapt fields you want to highlight in your report
    summary = by_product.reset_index().rename(columns={"revenue":"total_revenue", "units_sold":"total_units"})
    summary.to_csv(report_path, index=False)
    print(f"Saved report to {report_path}")

def plot_revenue(by_month, out_path):
    """Simple revenue over time plot."""
    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(by_month["month"].astype(str), by_month["revenue"], marker="o")
    ax.set_title("Revenue by Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close(fig)
    print(f"Saved plot to {out_path}")

def main():
    df = load_data(RAW_CSV)
    df = clean_data(df)
    overall, by_product, by_month = summary_statistics(df)
    save_report(overall, by_product, REPORT_CSV)
    plot_revenue(by_month, PLOT_PNG)
    # Print some summary to console for quick inspection
    print("=== Top products by revenue ===")
    print(by_product.head())
    print("\n=== Overall stats (units & revenue) ===")
    print(overall)

if __name__ == "__main__":
    main()
