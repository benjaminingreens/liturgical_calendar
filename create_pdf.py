import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, PageBreak

# Read the CSV into a DataFrame
csv_file = "liturgical_calendar_lexicon_2025.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Replace NaN values with empty strings
df = df.fillna("")

# Convert DataFrame to list of lists for the Table
data = [df.columns.tolist()] + df.values.tolist()

# Create the PDF
output_pdf = "readings.pdf"
pdf = SimpleDocTemplate(output_pdf, pagesize=landscape(A4))

# Function to split data into pages with header on each page
def split_data(data, rows_per_page):
    pages = []
    for i in range(0, len(data), rows_per_page):
        page_data = [data[0]] + data[i + 1 : i + 1 + rows_per_page]
        pages.append(page_data)
    return pages

# Split data into pages with a header on each page
rows_per_page = 20  # Adjust for your desired rows per page
pages = split_data(data, rows_per_page)

# Create tables for each page
elements = []
for page_data in pages:
    table = Table(page_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfe7ee")),  # Header background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#333333")),  # Header text color
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),                       # Center align all cells
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),            # Bold font for headers
        ("FONTSIZE", (0, 0), (-1, -1), 10),                         # Font size for all text
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7f9fc")),  # Row background
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),  # Grid lines
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f4f9")]),  # Alternate row colors
    ]))
    elements.append(table)
    elements.append(PageBreak())

# Remove the last PageBreak
if elements:
    elements.pop()

# Build the PDF
pdf.build(elements)

print(f"PDF generated: {output_pdf}")
