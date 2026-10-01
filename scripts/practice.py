import pandas as pd
import os

# This sets the working directory to wherever the script lives
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Loads the same CSV
df = pd.read_csv('../data/Sample - Superstore.csv', encoding = 'latin-1')

# Filters for orders where Profit is negative (loss-making orders)
df_loss = df[df['Profit'] < 0]

# Groups by Category and counts how many loss-making orders each category has
df_loss_category = df_loss.groupby('Category').agg(
    Loss_Order_Count = ('Order ID', 'count')
).sort_values('Loss_Order_Count', ascending = False)

# Prints the result
print("The number of loss-making orders:")
print(df_loss_category)

# Drill down - loss-making orders by Sub-Category
df_loss_subcategory = df_loss.groupby(['Category', 'Sub-Category']).agg(
    Loss_Order_Count = ('Order ID', 'count'),
    Total_Loss = ('Profit', 'sum')
).round(2).sort_values('Total_Loss', ascending = True)

print("\nLoss breakdown by Sub-Category:")
print(df_loss_subcategory)

# Save to Excel
output_path = os.path.join('..', 'data', 'loss_analysis.xlsx')

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    df_loss_category.to_excel(writer, sheet_name='By Category')
    df_loss_subcategory.to_excel(writer, sheet_name='By Sub-Category')
    
print(f"\nSaved to {output_path}")