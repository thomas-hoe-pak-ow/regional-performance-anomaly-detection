import pandas as pd
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the file
df = pd.read_csv("../data/Sample - Superstore.csv", encoding = "latin-1")
print("Number of rows: ", len(df))
print("Number of columns: ", len(df.columns))
print("Columns:", df.columns.to_list())
print("The columns are:", df.columns.to_list())
# print(df.shape)

# Dataset: Structure and data tyes
# df.info()

# Dataset: Statistical summary
# print(df.describe(include = "all"))

# Dataset: Missing values - column-by-column missing count
# print(df.isnull().sum())

# Dataset: Unique values categorical columns
# print(df["Region"].unique())
# print(df["Region"].nunique())

# Dataset: Duplicate rows
# print(df.duplicated().sum())

# Dataset: A peek at few rows
# print(df.head()) # first 5 rows
# print(df.sample(5)) # 5 random rows

# EDA: Top 3 by Category
# print(df.groupby("Category")["Sales"].sum()) # Just get the sum
# print(df.groupby("Category")["Sales"].sum().sort_values(ascending=False).head(3))

# EDA: <Sales, Quantity> by Region, Category, Sub-Category, Segment
# print(df.groupby(["Category","Sub-Category"])[["Sales","Quantity"]].sum().sort_values(by="Sales",ascending=False))
# EDA: Most Profitable by Region, Category, Sub-Category, Segment
# EDA: Most Discounted Products

