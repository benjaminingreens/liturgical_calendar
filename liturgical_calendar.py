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

    celebratory_days = []

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
    celebratory_days.append(principal_feasts)

    principal_holy_days = {
        "Ash Wednesday": ash_wednesday,
        "Maundy Thursday": maundy_thursday,
        "Good Friday": good_friday,
    }
    celebratory_days.append(principal_holy_days)

    festivals = {
        "Baptism of Christ": baptism_of_christ,
        "Christ the King": christ_the_king,
    }
    celebratory_days.append(festivals)

    lesser_festivals = {}
    celebratory_days.append(lesser_festivals)

    other_liturgical = {
        "Shrove Tuesday (Pancake Day)": shrove_tuesday,
        "Palm Sunday": palm_sunday,
        "Holy Monday": holy_monday,
        "Holy Tuesday": holy_tuesday,
        "Holy Wednesday": holy_wednesday,
        "Holy Saturday": holy_saturday,
        "Harvest": harvest,
    }
    celebratory_days.append(other_liturgical)

    other_other = {
        "Boxing Day": boxing_day,
        "New Year's Day": new_years_day,
        "St. Valentine's Day": valentines_day,
    }
    celebratory_days.append(other_other)

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

    return markdown.strip(), seasons, celebratory_days


year = 2025

# Example usage for the year 2024
markdown_content, seasons, celebratory_days = liturgical_calendar_markdown(year)

# Save the markdown to a file
if True:
    file_path = f"liturgical_calendar_{year}.md"
    with open(file_path, "w") as file:
        file.write(markdown_content)

    print(f"Markdown file saved as {file_path}")

# --- ADDITIONAL FUNCTIONALITY TO GENERATE LEXICON CSV ---

import csv


def combine_carried_over_readings(lexicon):
    """Combine 'Carried Over Days' with existing days while keeping the day name unchanged."""
    readings_by_date = {}

    for entry in lexicon:
        date, season, day_name, ot_reading, nt_reading = entry
        if date not in readings_by_date:
            readings_by_date[date] = {
                "season": season,
                "day_name": day_name,  # Keep the original day name
                "ot_reading": ot_reading,
                "nt_reading": nt_reading,
            }
        else:
            # Merge readings without modifying the day name
            if not readings_by_date[date]["nt_reading"] and nt_reading:
                readings_by_date[date]["nt_reading"] = nt_reading
            if not readings_by_date[date]["ot_reading"] and ot_reading:
                readings_by_date[date]["ot_reading"] = ot_reading

    # Reconstruct lexicon in sorted order by date
    combined_lexicon = [
        (
            date,
            values["season"],
            values["day_name"],
            values["ot_reading"],
            values["nt_reading"],
        )
        for date, values in sorted(readings_by_date.items())
    ]

    return combined_lexicon


def assign_readings(
    season_name,
    season_start,
    season_end,
    readings,
    reverse=False,
    baptism_adjust=False,
    carry_over_to=None,
    carry_over_readings=None,
    celebratory_days=celebratory_days,
):
    num_days = (season_end - season_start).days + 1
    daily_readings = readings.get(season_name, [])
    new_carry_over_readings = []

    (
        principal_feasts,
        principal_holy_days,
        festivals,
        lesser_festivals,
        other_liturgical,
        other_other,
    ) = celebratory_days

    # Combine all named days into a single dictionary
    named_days = {
        **principal_feasts,
        **principal_holy_days,
        **festivals,
        **lesser_festivals,
        **other_liturgical,
        **other_other,
    }

    week_number = 0  # Internal week counter
    assigned_readings = []

    for i in range(num_days):
        current_date = season_start + timedelta(days=i)
        ot_reading, nt_reading = "", ""

        # Determine the name of the day
        if current_date in named_days.values():
            day_name = [key for key, value in named_days.items() if value == current_date][0]
            # If it's a Sunday, increment the week count for subsequent weekdays
            if current_date.weekday() == 6:
                week_number += 1
        else:
            # For Sundays, increment the week counter
            if current_date.weekday() == 6:  # Sunday
                week_number += 1
                day_name = f"{week_number} Sunday of {season_name}"
            else:
                # Use the most recent Sunday week number for weekdays
                day_of_week = current_date.strftime("%A")
                day_name = f"{day_of_week} of Week {week_number} of {season_name}"

        # Use readings if provided
        if i < len(daily_readings):
            ot_reading, nt_reading = daily_readings[i][1:]

        assigned_readings.append(
            (current_date, season_name, day_name, ot_reading, nt_reading)
        )

    # Handle carry-over readings for the next season
    if carry_over_to is not None and carry_over_readings is not None:
        carry_over_readings.extend(new_carry_over_readings)
    elif carry_over_to is not None:
        carry_over_readings = new_carry_over_readings

    return assigned_readings, carry_over_readings


# Add reverse flags dynamically
def add_reverse_flags(seasons):
    reverse_mapping = {
        "Advent": True,
        "Christmas": False,
        "Epiphany": False,
        "First Ordinary Time": False,
        "Lent": False,
        "Easter": False,
        "Second Ordinary Time": False,
    }
    return [
        (season_name, start, end, reverse_mapping.get(season_name, False))
        for season_name, start, end in seasons
    ]


def generate_lexicon_csv(year, readings_file, output_file):
    # Get seasons by calling the liturgical_calendar_markdown function
    _, raw_seasons, celebratory_days = liturgical_calendar_markdown(year)

    # Debug: Print seasons
    print(f"Raw seasons: {raw_seasons}")

    # Add reverse flags to the seasons
    seasons = add_reverse_flags(raw_seasons)

    # Debug: Print seasons with reverse flags
    print(f"Seasons with reverse flags: {seasons}")

    # Load readings from the CSV file
    readings = {}
    with open(readings_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            season = row["SEASON"].strip()
            day = row.get("DAY", "").strip() if row.get("DAY") else ""
            ot_reading = row["OT READING"].strip() if row["OT READING"] else ""
            nt_reading = row["NT YEAR A"].strip() if row["NT YEAR A"] else ""
            if season not in readings:
                readings[season] = []
            readings[season].append((day, ot_reading, nt_reading))

    # Debug: Print loaded readings
    print(f"Loaded readings: {readings}")

    # Assign readings to each date
    lexicon = []
    carry_over_readings = []
    for season_name, season_start, season_end, reverse in seasons:
        baptism_adjust = season_name == "Epiphany"
        carry_over_to = "Lent" if season_name == "First Ordinary Time" else None
        season_readings, carry_over_readings = assign_readings(
            season_name,
            season_start,
            season_end,
            readings,
            reverse=reverse,
            baptism_adjust=baptism_adjust,
            carry_over_to=carry_over_to,
            carry_over_readings=carry_over_readings,
            celebratory_days=celebratory_days,
        )
        lexicon.extend(season_readings)

        # Debug: Print assigned readings for the season
        print(f"Assigned readings for {season_name}:")
        for reading in season_readings:
            print(reading)

        # Debug: Print carry-over readings after assignment
        print(f"Carry-over readings after {season_name}: {carry_over_readings}")

    # Append carry-over readings to Lent
    lent_start = [s for s in seasons if s[0] == "Lent"][0][1]
    for i, (day_name, _, nt_reading) in enumerate(carry_over_readings):
        lexicon.append(
            (lent_start + timedelta(days=i), "Lent", day_name, "", nt_reading)
        )

        # Debug: Print carry-over reading being appended
        print(
            f"Appending carry-over reading to Lent: {lent_start + timedelta(days=i)}, {day_name}, {nt_reading}"
        )

    # Combine 'Carried Over Days' with existing days where there is no clash
    lexicon = combine_carried_over_readings(lexicon)

    # Debug: Print lexicon after combining carried-over readings
    print("Lexicon after combining carried-over readings:")
    for entry in lexicon:
        print(entry)

    # Write the lexicon to a CSV
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Season", "Day Name", "OT Reading", "NT Reading"])
        for entry in sorted(lexicon, key=lambda x: x[0]):
            writer.writerow(entry)

    print(f"Lexicon CSV saved as {output_file}")


# Main function to generate lexicon CSV
def main(year):
    year = year
    readings_file = "bible_plan.csv"  # Replace with your readings CSV
    output_file = f"liturgical_calendar_lexicon_{year}.csv"
    generate_lexicon_csv(year, readings_file, output_file)


if __name__ == "__main__":
    main(year)
