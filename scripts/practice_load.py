import pandas as pd
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Load the data file
df = pd.read_csv("../data/Sample - Superstore.csv", encoding ="latin-1")
print("Number of rows: ", len(df))
print("Number of columns: ", len(df.columns))
print("The columns: ", df.columns.to_list())