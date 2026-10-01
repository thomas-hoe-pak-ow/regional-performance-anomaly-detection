import pandas as pd
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the CSV
df = pd.read_csv('../data/Sample - Superstore.csv', encoding='latin-1')

# Filter for loss-making orders
df_loss = df[df['Profit']<0]

# Group by Region and Category
df_loss_region_category = df_loss.groupby(['Region','Category']).agg(
    Loss_Order_Count = ('Order ID', 'count'),
    Total_Loss = ('Profit', 'sum')
).round(2).sort_values('Total_Loss', ascending=True)

# Show both Loss_Order_Count and Total_Loss
# Sort by Total_Loss ascending
print('Loss Making Orders and Total Loss:')
print(df_loss_region_category)

# Save to region_loss.xlsx
output_path = os.path.join('..','data','region_loss_2.xlsx')
df_loss_region_category.to_excel(output_path)
print(f"\nFile is saved to {output_path}.")