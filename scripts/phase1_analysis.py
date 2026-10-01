import pandas as pd

# ── 1. LOAD ──────────────────────────────────────────────────────────────────
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin-1")
print("Rows:", len(df))
print("Columns:", df.columns.tolist())

# ── 2. INSPECT ───────────────────────────────────────────────────────────────
print("\nFirst 3 rows:")
print(df.head(3))

# ── 3. FILTER ────────────────────────────────────────────────────────────────
# Keep only rows where Sales > 500
high_sales = df[df["Sales"] > 500]
print(f"\nOrders with Sales > 500: {len(high_sales)}")

# ── 4. SUMMARISE ─────────────────────────────────────────────────────────────
# Total sales and average profit by Region — same idea as GROUP BY in SQL
summary = df.groupby("Region").agg(
    Total_Sales   = ("Sales",  "sum"),
    Avg_Profit    = ("Profit", "mean"),
    Order_Count   = ("Sales",  "count")
).round(2)

print("\nSales summary by Region:")
print(summary)

# ── 5. SAVE ──────────────────────────────────────────────────────────────────
output_path = r"C:\Users\thoma\OneDrive\Desktop\python-learning\data\region_summary.xlsx"
summary.to_excel(output_path)
print(f"\nDone. File saved to {output_path}")