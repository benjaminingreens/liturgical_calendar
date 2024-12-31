import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, PageBreak
from textwrap import wrap

# Read the CSV into a DataFrame
csv_file = "liturgical_calendar_lexicon_2025.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Replace NaN values with empty strings
df = df.fillna("")

# Highlighting rules
muted_red_days = [
    "CHRISTMAS DAY", "EPIPHANY", "CANDLEMAS", "ANNUNCIATION", "EASTER SUNDAY",
    "ASCENSION DAY", "PENTECOST/WHITSUNDAY", "TRINITY SUNDAY", "ALL SAINTS' DAY"
]
muted_blue_days = [
    "Baptism of Christ", "Christ the King", "Ash Wednesday", "Maundy Thursday", "Good Friday"
]
muted_grey_days = [
    "Shrove Tuesday (Pancake Day)", "Palm Sunday", "Holy Monday", "Holy Tuesday", 
    "Holy Wednesday", "Holy Saturday", "Harvest"
]

# Function to wrap text to fit column width
def wrap_text(text, max_width):
    return "\n".join(wrap(str(text), max_width))

# Calculate column widths dynamically for each page
def calculate_column_widths(page_data, max_page_width=750, min_table_width=700):
    col_widths = [max(len(str(cell)) for cell in col) * 6 for col in zip(*page_data)]
    total_width = sum(col_widths)

    # Ensure a minimum table width
    if total_width < min_table_width:
        scale_factor = min_table_width / total_width
        col_widths = [int(width * scale_factor) for width in col_widths]

    # Adjust "NT Reading" and "OT Reading" to wrap if total width exceeds page width
    if total_width > max_page_width:
        nt_index = page_data[0].index("NT Reading")
        ot_index = page_data[0].index("OT Reading")
        for row in page_data[1:]:
            row[nt_index] = wrap_text(row[nt_index], 30)
            row[ot_index] = wrap_text(row[ot_index], 30)

        # Recalculate column widths after wrapping
        col_widths = [max(len(str(cell)) for cell in col) * 6 for col in zip(*page_data)]

    return col_widths

# Function to split data into pages with header on each page and ensure full pages
def split_data(data, max_page_height, max_page_width):
    pages = []
    current_page = [data[0]]  # Start with header row
    current_height = 30  # Initial height for header row
    row_height = 20  # Estimate row height

    for row in data[1:]:
        if current_height + row_height <= max_page_height:
            current_page.append(row)
            current_height += row_height
        else:
            # Calculate column widths for current page and add to pages
            col_widths = calculate_column_widths(current_page, max_page_width)
            pages.append((current_page, col_widths))
            current_page = [data[0], row]  # Start new page with header
            current_height = 30 + row_height

    if len(current_page) > 1:
        col_widths = calculate_column_widths(current_page, max_page_width)
        pages.append((current_page, col_widths))

    return pages

# Convert DataFrame to list of lists for the Table
data = [df.columns.tolist()] + df.values.tolist()

# Adjust the "Day Name" column dynamically
day_name_index = data[0].index("Day Name")
for row in data[1:]:
    row[day_name_index] = wrap_text(row[day_name_index], 50)

# Split data into pages
max_page_height = 550
max_page_width = 750
pages = split_data(data, max_page_height, max_page_width)

# Create the PDF
output_pdf = "readings.pdf"
pdf = SimpleDocTemplate(output_pdf, pagesize=landscape(A4))

# Create tables for each page
elements = []

for page_data, col_widths in pages:
    table = Table(page_data, colWidths=col_widths)  # Adjust column widths dynamically for the page

    # Style table
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfe7ee")),  # Header background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#333333")),  # Header text color
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),                       # Center align all cells
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),            # Bold font for headers
        ("FONTSIZE", (0, 0), (-1, -1), 10),                         # Font size for all text
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7f9fc")),  # Row background
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),  # Grid lines
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f4f9")]),  # Alternate row colors
    ])

    # Highlight rows based on "Day Name"
    for i, row in enumerate(page_data[1:], start=1):  # Skip header row
        day_name = row[page_data[0].index("Day Name")]
        if any(day in day_name for day in muted_red_days):
            style.add("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f8d7da"))
        elif any(day in day_name for day in muted_blue_days):
            style.add("BACKGROUND", (0, i), (-1, i), colors.HexColor("#d1ecf1"))
        elif any(day in day_name for day in muted_grey_days):
            style.add("BACKGROUND", (0, i), (-1, i), colors.HexColor("#e2e3e5"))

    table.setStyle(style)
    elements.append(table)
    elements.append(PageBreak())

# Remove the last PageBreak
if elements:
    elements.pop()

# Build the PDF
pdf.build(elements)

print(f"PDF generated: {output_pdf}")

