import datetime
from datetime import timedelta

# Add weeks
# Add birthdays
# Add anniversaries
# Should I add more festivals and lesser festivals? Only have baptism and christ the king right now
# Demarcate other liturgical and other other dates from all other dates


# Function to calculate Easter based on the year (Western Christianity)
def calculate_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)


# Function to find the first Sunday after a given date
def first_sunday_after(date):
    weekday = date.weekday()
    return date + timedelta(days=(6 - weekday) if weekday != 6 else 0)


# Function to calculate the First Sunday of Advent
def first_sunday_of_advent(year):
    date = datetime.date(year, 11, 27)
    while date.weekday() != 6:  # While it's not Sunday
        date += timedelta(days=1)
    return date


# Function to calculate Annunciation date, adjusting if it falls in Holy Week
def calculate_annunciation(year, easter):
    annunciation = datetime.date(year, 3, 25)
    holy_week_start = easter - timedelta(days=6)
    holy_week_end = easter - timedelta(days=1)

    if holy_week_start <= annunciation <= holy_week_end:
        return easter + timedelta(days=8)
    else:
        return annunciation


# Function to generate the liturgical calendar in markdown format
def liturgical_calendar_markdown(year):

    # Date of easter
    easter = calculate_easter(year)

    # Beginning of liturgical year
    last_year = year - 1
    first_advent_sunday = first_sunday_of_advent(last_year)
    end_of_september = datetime.date(year, 9, 30)

    # Fixed principal feasts
    christmas_day = datetime.date(year - 1, 12, 25)
    epiphany = datetime.date(year, 1, 6)
    candlemas = datetime.date(year, 2, 2)
    all_saints_day = datetime.date(year, 11, 1)

    # Moveable principal feasts
    annunciation = calculate_annunciation(year, easter)
    ascension_day = easter + timedelta(days=39)
    pentecost = easter + timedelta(days=49)
    trinity_sunday = pentecost + timedelta(days=7)

    # Moveable principal holy days
    ash_wednesday = easter - timedelta(days=46)
    maundy_thursday = easter - timedelta(days=3)
    good_friday = easter - timedelta(days=2)

    # This is required to calculate christ the king
    next_advent_sunday = first_sunday_of_advent(year)

    # Moveable festivals
    baptism_of_christ = first_sunday_after(epiphany)
    christ_the_king = next_advent_sunday - timedelta(days=7)

    # Moveable other
    shrove_tuesday = easter - timedelta(days=47)
    palm_sunday = easter - timedelta(days=7)
    holy_monday = easter - timedelta(days=6)
    holy_tuesday = easter - timedelta(days=5)
    holy_wednesday = easter - timedelta(days=4)
    holy_saturday = easter - timedelta(days=1)
    harvest = first_sunday_after(end_of_september)

    # Fixed other other
    boxing_day = datetime.date(year - 1, 12, 26)
    new_years_day = datetime.date(year, 1, 1)
    valentines_day = datetime.date(year, 2, 14)

    # Season timings
    advent_start = first_advent_sunday
    lent_start = ash_wednesday
    easter_start = easter
    ordinary_time_first_start = candlemas + timedelta(days=1)
    ordinary_time_second_start = pentecost + timedelta(days=1)
    ordinary_time_second_end = christ_the_king + timedelta(days=6)

    principal_feasts = {
        "CHRISTMAS DAY": christmas_day,
        "EPIPHANY": epiphany,
        "CANDLEMAS": candlemas,
        "ANNUNCIATION": annunciation,
        "EASTER SUNDAY": easter,
        "ASCENSION DAY": ascension_day,
        "PENTECOST/WHITSUNDAY": pentecost,
        "TRINITY SUNDAY": trinity_sunday,
        "ALL SAINTS' DAY": all_saints_day,
    }

    principal_holy_days = {
        "Ash Wednesday": ash_wednesday,
        "Maundy Thursday": maundy_thursday,
        "Good Friday": good_friday,
    }

    festivals = {
        "Baptism of Christ": baptism_of_christ,
        "Christ the King": christ_the_king,
    }

    lesser_festivals = {}

    other_liturgical = {
        "Shrove Tuesday (Pancake Day)": shrove_tuesday,
        "Palm Sunday": palm_sunday,
        "Holy Monday": holy_monday,
        "Holy Tuesday": holy_tuesday,
        "Holy Wednesday": holy_wednesday,
        "Holy Saturday": holy_saturday,
        "Harvest": harvest,
    }

    other_other = {
        "Boxing Day": boxing_day,
        "New Year's Day": new_years_day,
        "St. Valentine's Day": valentines_day,
    }

    seasons = [
        ("Advent", advent_start, christmas_day - timedelta(days=1)),
        ("Christmas", christmas_day, epiphany - timedelta(days=1)),
        ("Epiphany", epiphany, ordinary_time_first_start - timedelta(days=1)),
        (
            "First Ordinary Time",
            ordinary_time_first_start,
            ash_wednesday - timedelta(days=1),
        ),
        ("Lent", lent_start, easter_start - timedelta(days=1)),
        ("Easter", easter_start, pentecost),
        ("Second Ordinary Time", ordinary_time_second_start, ordinary_time_second_end),
    ]

    # Markdown generation
    markdown = f"# Liturgical Calendar for {year}\n"
    markdown += """
## Key\n
**FEASTS**  
**Holy Days**  
***Festivals***  
*Lesser Festivals*  
Other Days\n
"""

    for season, season_start, season_end in seasons:
        markdown += f"## {season}\n\n"
        markdown += f"Starts {season_start.strftime('%A, %d %B %Y')}\n\n"

        # Collect and sort all events for the season
        events = []

        for feast, feast_date in principal_feasts.items():
            if season_start <= feast_date <= season_end:
                print(f"Including {feast} on {feast_date} in {season}")
                events.append((feast_date, f"**{feast}**"))

        for feast, feast_date in principal_holy_days.items():
            if season_start <= feast_date <= season_end:
                print(f"Including {feast} on {feast_date} in {season}")
                events.append((feast_date, f"**{feast}**"))

        for feast, feast_date in festivals.items():
            if season_start <= feast_date <= season_end:
                print(f"Including {feast} on {feast_date} in {season}")
                events.append((feast_date, f"***{feast}***"))

        for feast, feast_date in lesser_festivals.items():
            if season_start <= feast_date <= season_end:
                print(f"Including {feast} on {feast_date} in {season}")
                events.append((feast_date, f"*{feast}*"))

        for feast, feast_date in other_liturgical.items():
            if season_start <= feast_date <= season_end:
                print(f"Including {feast} on {feast_date} in {season}")
                events.append((feast_date, f"{feast}"))

        for feast, feast_date in other_other.items():
            if season_start <= feast_date <= season_end:
                print(f"Including {feast} on {feast_date} in {season}")
                events.append((feast_date, f"{feast}"))

        if events:
            # Sort events by date and add them to markdown
            events.sort(key=lambda x: x[0])
            for event_date, event in events:
                markdown += f"- {event}: {event_date.strftime('%A, %d %B %Y')}\n"

            markdown += "\n"  # Newline after each season

    return markdown.strip()

year = 2025

# Example usage for the year 2024
markdown_content = liturgical_calendar_markdown(year)

# Save the markdown to a file
file_path = f"liturgical_calendar_{year}.md"
with open(file_path, "w") as file:
    file.write(markdown_content)

print(f"Markdown file saved as {file_path}")
