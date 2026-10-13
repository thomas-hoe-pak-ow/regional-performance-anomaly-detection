import pandas as pd
import os
from flags import iqr_bounds, flag_high_values
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the file
df = pd.read_csv("../data/Sample - Superstore.csv", encoding = "latin-1")
print("Number of rows: ", len(df))
print("Number of columns: ", len(df.columns))
print("Columns:", df.columns.to_list())
print("The columns are:", df.columns.to_list())
print("The shape of the dataset")
print(df.shape)

# Dataset: Structure and data tyes
# print("The structure and data types:")
# df.info()

# Dataset: Statistical summary
# print("The statistical summary:")
# print(df.describe(include = "all"))

# Dataset: Missing values - column-by-column missing count
# print("The column-by-column missing values:")
# print(df.isnull().sum())

# Dataset: A peek at few rows
# print("A look at 5 rows:")
# print(df.head()) # first 5 rows
# print(df.sample(5)) # 5 random rows

# From Superstore dataset, check for outlier by using interquartile range (IQR) method

def flag_region_subcategory_outliers(df):
    """
    Aggregates Margin by Region + Sub-Category, then flags which combos
    are outliers using iqr_bounds().
    """
    # Step 1: groupby(['Region', 'Sub-Category'])[['Sales','Profit'], aggregate with .sum()
    # Use .reset_index() so Region/Sub-Category become columns again.
    grouped = df.groupby(['Region', 'Sub-Category'])[['Sales', 'Profit']].sum().reset_index()
    grouped['Margin'] = grouped['Profit'] / grouped['Sales']

    # Step 2: call iqr_bounds() on the aggregated Margin column
    lower, upper = iqr_bounds(grouped['Margin'])

    # Step 3: add an 'is_outlier' column: True where Margin is outside [lower, upper]
    grouped['is_outlier'] = (grouped['Margin'] < lower) | (grouped['Margin'] > upper)

    return grouped

# print(flag_region_subcategory_outliers(df))

# result = flag_region_subcategory_outliers(df)
# outliers = result[result['is_outlier']]

# print(outliers.sort_values('Margin'))
# print(len(outliers))

# lower, upper = iqr_bounds(result['Margin'])
# print(f"Bounds: {lower:.3f} to {upper:.3f}")
# print(f"Actual range: {result['Margin'].min():.3f} to {result['Margin'].max():.3f}")

# Results markdown
# Looking at margin by Region_Sub-Category, there is no outlier detected.
# This is likely because of the margin value being aggregated at Region_Sub-Category level, smoothing out the number in the process
result = flag_high_values(df, 'Category', 'Discount')
print(result.columns.tolist())
print(result['high_discount'].value_counts())
print(result[result['high_discount']][['Category', 'Discount']].head(10))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── 1. LOAD TEMPLATE ─────────────────────────────────────────────────────────
template_path = os.path.join('..', 'data', 'template.pptx')
prs = Presentation(template_path)

# ── 2. ACCESS SLIDE 1 ────────────────────────────────────────────────────────
slide = prs.slides[0]

# ── 3. ADD A TITLE ───────────────────────────────────────────────────────────
# (new — previous version relied on the template's own title, if any)
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
tf_title = title_box.text_frame
tf_title.text = 'Regional Performance Anomaly Detection — Key Findings'
tf_title.paragraphs[0].runs[0].font.size = Pt(24)
tf_title.paragraphs[0].runs[0].font.bold = True

# ── 4. INSERT CHART IMAGE ────────────────────────────────────────────────────
# (changed: new chart file, and shifted down/shrunk slightly to leave room
#  for the findings text below it)
chart_path = os.path.join('..', 'charts', 'discount_by_category.png')

left   = Inches(0.5)
top    = Inches(1.3)
width  = Inches(9)
height = Inches(4.2)

slide.shapes.add_picture(chart_path, left, top, width, height)

# ── 5. ADD FINDINGS SUMMARY ──────────────────────────────────────────────────
# (new — the actual "so what" for someone reading the slide)
findings_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.6), Inches(9), Inches(1.1))
tf_findings = findings_box.text_frame
tf_findings.word_wrap = True

findings_text = (
    "Q1 (Region \u00d7 Sub-Category margin): no statistical outliers detected \u2014 "
    "expected, since aggregation smooths extremes.\n"
    "Q2 (order-level discount): 703 of 9,994 orders (~7%) flagged as unusually high "
    "discount vs. their Category norm \u2014 in Office Supplies (70\u201380%) and Technology (70%)."
)
tf_findings.text = findings_text
for para in tf_findings.paragraphs:
    para.runs[0].font.size = Pt(12)

# ── 6. ADD A SUBTITLE / SOURCE LINE ─────────────────────────────────────────
txBox = slide.shapes.add_textbox(Inches(0.5), Inches(6.9), Inches(9), Inches(0.4))
tf = txBox.text_frame
tf.text = 'Source: Superstore Sales Dataset | Method: IQR-based outlier detection'
tf.paragraphs[0].runs[0].font.size = Pt(9)
tf.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# ── 7. SAVE OUTPUT ───────────────────────────────────────────────────────────
output_path = os.path.join('..', 'data', 'anomaly_detection_summary.pptx')
# prs.save(output_path)
# print(f"Presentation saved to {output_path}")


# ── 2.2. ACCESS SLIDE 2 ────────────────────────────────────────────────────────
slide2 = prs.slides.add_slide(slide.slide_layout)

# ── 2.3. ADD A TITLE ───────────────────────────────────────────────────────────
# (new — previous version relied on the template's own title, if any)
title_box2 = slide2.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
tf_title2 = title_box2.text_frame
tf_title2.text = 'Regional Performance Anomaly Detection — Key Findings #2'
tf_title2.paragraphs[0].runs[0].font.size = Pt(24)
tf_title2.paragraphs[0].runs[0].font.bold = True

# ── 2.4. INSERT CHART IMAGE ────────────────────────────────────────────────────
# (changed: new chart file, and shifted down/shrunk slightly to leave room
#  for the findings text below it)
chart_path = os.path.join('..', 'charts', 'profit_by_region_category.png')

left   = Inches(0.5)
top    = Inches(1.3)
width  = Inches(9)
height = Inches(4.2)

slide2.shapes.add_picture(chart_path, left, top, width, height)

# ── 2.5. ADD FINDINGS SUMMARY ──────────────────────────────────────────────────
# (new — the actual "so what" for someone reading the slide)
findings_box2 = slide2.shapes.add_textbox(Inches(0.5), Inches(5.6), Inches(9), Inches(1.1))
tf_findings2 = findings_box2.text_frame
tf_findings2.word_wrap = True

findings_text2 = (
    "(Region \u00d7 Category profit): no statistical outliers detected \u2014 "
    "similarly expected, since aggregation smooths extremes."
)
tf_findings2.text = findings_text2
for para in tf_findings2.paragraphs:
    para.runs[0].font.size = Pt(12)

# ── 6. ADD A SUBTITLE / SOURCE LINE ─────────────────────────────────────────
txBox2 = slide2.shapes.add_textbox(Inches(0.5), Inches(6.9), Inches(9), Inches(0.4))
tf2 = txBox2.text_frame
tf2.text = 'Source: Superstore Sales Dataset | Method: IQR-based outlier detection'
tf2.paragraphs[0].runs[0].font.size = Pt(9)
tf2.paragraphs[0].runs[0].font.color.rgb = RGBColor(0x88, 0x88, 0x88)

# ── 7. SAVE OUTPUT ───────────────────────────────────────────────────────────
output_path = os.path.join('..', 'data', 'anomaly_detection_summary.pptx')
# Remove empty placeholders left by the template layout
for s in prs.slides:
    for shape in list(s.placeholders):
        if shape.has_text_frame and not shape.text_frame.text.strip():
            shape._element.getparent().remove(shape._element)
            
prs.save(output_path)
print(f"Presentation saved to {output_path}")