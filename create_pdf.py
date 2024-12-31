import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, PageBreak
from textwrap import wrap as space_wrap
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch

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

def split_data_by_season(data):
    """
    Split data into pages based on changes in the 'Season' column.
    """
    header_row = data[0]
    season_index = header_row.index("Season")
    pages = []
    current_page = [header_row]
    current_season = None

    for row in data[1:]:
        row_season = row[season_index]
        if row_season != current_season:
            # Start a new page if the season changes
            if len(current_page) > 1:  # Avoid adding empty pages
                pages.append(current_page)
            current_page = [header_row]
            current_season = row_season

        current_page.append(row)

    if len(current_page) > 1:  # Add the last page if it has any rows
        pages.append(current_page)

    return pages

def get_row_height(row, col_widths, font_size=10, leading=12):
    """
    Calculate the height of a row based on the wrapped content in each cell.
    """
    style = ParagraphStyle("default", fontName="Helvetica", fontSize=font_size, leading=leading)
    max_lines = 0
    for cell, col_width in zip(row, col_widths):
        para = Paragraph(wrap_text(cell, col_width), style)
        _, height = para.wrap(col_width, inch)
        max_lines = max(max_lines, height / leading)
    return max_lines * leading

def wrap_text(text, max_width):
    text = str(text).strip()
    if len(text) <= max_width // 6:  # Approximate width in characters
        return text
    parts = text.split(';')
    wrapped_by_semicolons = [
        part.strip() + (';' if i < len(parts) - 1 else '') for i, part in enumerate(parts)
    ]
    fully_wrapped = []
    for line in wrapped_by_semicolons:
        if len(line) > max_width // 6:
            fully_wrapped.extend(space_wrap(line, width=max_width // 6))
        else:
            fully_wrapped.append(line)
    return "\n".join(fully_wrapped)

def calculate_column_widths(data, max_page_width=750, min_table_width=700):
    buffer = 10
    header = data[0]
    header_widths = [len(str(cell)) * 6 + buffer for cell in header]

    col_widths = [
        max(max(len(str(cell)) for cell in col) * 6 + buffer, header_width)
        for col, header_width in zip(zip(*data), header_widths)
    ]

    total_width = sum(col_widths)
    if total_width < min_table_width:
        scale_factor = min_table_width / total_width
        col_widths = [int(width * scale_factor) for width in col_widths]
    elif total_width > max_page_width:
        ot_index = header.index("OT Reading")
        nt_index = header.index("NT Reading")
        excess_width = total_width - max_page_width
        ot_width = col_widths[ot_index]
        nt_width = col_widths[nt_index]
        total_reducible = ot_width + nt_width
        if total_reducible > 0:
            reduction_factor = excess_width / total_reducible
            col_widths[ot_index] -= int(ot_width * reduction_factor)
            col_widths[nt_index] -= int(nt_width * reduction_factor)
        min_col_width = max(header_widths)
        col_widths[ot_index] = max(col_widths[ot_index], min_col_width)
        col_widths[nt_index] = max(col_widths[nt_index], min_col_width)

    # Ensure no column is smaller than its header text
    col_widths = [
        max(width, header_width) for width, header_width in zip(col_widths, header_widths)
    ]

    return col_widths

def split_data(data, col_widths, max_page_height=550, font_size=10, leading=12):
    """
    Split data into pages based on dynamic row heights, ensuring every page starts with a header.
    """
    header_row = data[0]
    pages = []
    current_page = [header_row]
    current_height = get_row_height(header_row, col_widths, font_size, leading)  # Header row height

    for row in data[1:]:
        row_height = get_row_height(row, col_widths, font_size, leading)
        
        # Check if adding the row would exceed the page height
        if current_height + row_height > max_page_height:
            pages.append(current_page)  # Save the current page
            current_page = [header_row]  # Start a new page with the header
            current_height = get_row_height(header_row, col_widths, font_size, leading)

        # Add the row to the current page
        current_page.append(row)
        current_height += row_height

    if len(current_page) > 1:  # Add the last page if it has any rows
        pages.append(current_page)

    return pages

data = [df.columns.tolist()] + df.values.tolist()
max_page_height = 550
max_page_width = 700

# Calculate column widths before splitting data
col_widths = calculate_column_widths(data, max_page_width)

# Split data into pages using the calculated column widths
# pages = split_data(data, col_widths, max_page_height)
pages = split_data_by_season(data)

# Generate the PDF with the split pages
output_pdf = "readings.pdf"
pdf = SimpleDocTemplate(output_pdf, pagesize=landscape(A4))
elements = []
for page_data in pages:
    col_widths = calculate_column_widths(page_data, max_page_width)
    nt_index = page_data[0].index("NT Reading")
    ot_index = page_data[0].index("OT Reading")
    for row in page_data[1:]:
        row[nt_index] = wrap_text(row[nt_index], col_widths[nt_index])
        row[ot_index] = wrap_text(row[ot_index], col_widths[ot_index])
    table = Table(page_data, colWidths=col_widths, repeatRows=1)  # Repeat header row
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dfe7ee")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#333333")),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Vertically center all text
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f7f9fc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f4f9")]),
    ])
    day_name_index = page_data[0].index("Day Name")
    for i, row in enumerate(page_data[1:], start=1):
        day_name = row[day_name_index]
        if any(day in day_name for day in muted_red_days):
            style.add("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f8d7da"))
        elif any(day in day_name for day in muted_blue_days):
            style.add("BACKGROUND", (0, i), (-1, i), colors.HexColor("#d1ecf1"))
        elif any(day in day_name for day in muted_grey_days):
            style.add("BACKGROUND", (0, i), (-1, i), colors.HexColor("#e2e3e5"))
    table.setStyle(style)
    elements.append(table)
    elements.append(PageBreak())

if elements:
    elements.pop()  # Remove the last PageBreak

pdf.build(elements)
print(f"PDF generated: {output_pdf}")

