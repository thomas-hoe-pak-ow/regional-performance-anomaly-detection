import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load and prepare data
df = pd.read_csv('../data/Sample - Superstore.csv', encoding = 'latin-1')

df_loss = df[df['Profit'] < 0]

summary = df_loss.groupby('Sub-Category').agg(
    Total_Loss = ('Profit', 'sum')
).round(2).sort_values('Total_Loss', ascending=False)

# Build chart
fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(
    summary.index,
    summary['Total_Loss'],
    color='#D94F3D'
)

# Labels and formatting
ax.set_title('Total Loss by Sub-Category', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Total Loss (USD)', fontsize=11)
ax.set_ylabel('Sub-Category', fontsize=11)
ax.axvline(x=0, color='black', linewidth=0.8)

for bar, value in zip(ax.patches, summary['Total_Loss']):
    ax.text(
        value - 500,
        bar.get_y() + bar.get_height() / 2,
        f'${value:,.0f}',
        va='center', ha='right',
        fontsize=9, color='white'
    )

plt.tight_layout()

# Save
output_path = os.path.join('..', 'data', 'loss_by_subcategory.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Chart saved to {output_path}")