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
        date, season, day_name, meditation, ot_reading, nt_reading = entry
        if date not in readings_by_date:
            readings_by_date[date] = {
                "season": season,
                "day_name": day_name,  # Keep the original day name
                "meditation": meditation,
                "ot_reading": ot_reading,
                "nt_reading": nt_reading,
            }
        else:
            # Merge readings without modifying the day name
            if not readings_by_date[date]["nt_reading"] and nt_reading:
                readings_by_date[date]["nt_reading"] = nt_reading
            if not readings_by_date[date]["ot_reading"] and ot_reading:
                readings_by_date[date]["ot_reading"] = ot_reading
            if not readings_by_date[date]["meditation"] and meditation:
                readings_by_date[date]["meditation"] = meditation

    # Reconstruct lexicon in sorted order by date
    combined_lexicon = [
        (
            date,
            values["season"],
            values["day_name"],
            values["meditation"],
            values["ot_reading"],
            values["nt_reading"],
        )
        for date, values in sorted(readings_by_date.items())
    ]

    return combined_lexicon

def adjust_annunciation_readings(lexicon, annunciation_date):
    """Adjust readings around Annunciation based on provided logic."""
    adjusted_lexicon = []
    readings_by_date = {entry[0]: entry for entry in lexicon}

    # Determine OT readings for days around Annunciation
    days = [
        annunciation_date - timedelta(days=2),
        annunciation_date - timedelta(days=1),
        annunciation_date,
        annunciation_date + timedelta(days=1),
        annunciation_date + timedelta(days=2),
    ]

    # Collect OT readings for the relevant days
    ot_readings = {day: readings_by_date.get(day, (None, None, None, None, "", None))[4] for day in days}

    # Handle the case where Annunciation has no readings
    if not ot_readings[annunciation_date]:
        ot_readings[annunciation_date] = ""

    # Split Annunciation readings if present
    if ot_readings[annunciation_date]:
        chapters = ot_readings[annunciation_date].split(",")
        mid = len(chapters) // 2
        above_split = ",".join(chapters[:mid])
        below_split = ",".join(chapters[mid:])
    else:
        above_split = below_split = ""

    # Combine readings
    combined_readings_before = ot_readings[days[0]]
    if ot_readings[days[1]]:
        combined_readings_before = (combined_readings_before + "," + ot_readings[days[1]]).strip(",")
    combined_readings_before = (combined_readings_before + "," + above_split).strip(",")

    combined_readings_after = below_split
    if ot_readings[days[3]]:
        combined_readings_after = (combined_readings_after + "," + ot_readings[days[3]]).strip(",")
    combined_readings_after = (combined_readings_after + "," + ot_readings[days[4]]).strip(",")

    # Update readings in the lexicon
    if combined_readings_before:
        readings_by_date[days[0]] = (
            days[0],
            readings_by_date.get(days[0], (None, None, None, None, "", None))[1],
            readings_by_date.get(days[0], (None, None, None, None, "", None))[2],
            readings_by_date.get(days[0], (None, None, None, None, "", None))[3],
            combined_readings_before,
            readings_by_date.get(days[0], (None, None, None, None, "", None))[5],
        )

    if combined_readings_after:
        readings_by_date[days[4]] = (
            days[4],
            readings_by_date.get(days[4], (None, None, None, None, "", None))[1],
            readings_by_date.get(days[4], (None, None, None, None, "", None))[2],
            readings_by_date.get(days[4], (None, None, None, None, "", None))[3],
            combined_readings_after,
            readings_by_date.get(days[4], (None, None, None, None, "", None))[5],
        )

    # Clear meditations for Annunciation and adjacent days, and update specific readings
    for day in [days[1], annunciation_date, days[3]]:
        readings_by_date[day] = (
            day,
            readings_by_date.get(day, (None, None, None, None, "", None))[1],
            readings_by_date.get(day, (None, None, None, None, "", None))[2],
            "",  # Clear meditation
            "",  # Clear OT reading
            readings_by_date.get(day, (None, None, None, None, "", None))[5],
        )

    # Add specific OT and NT readings
    readings_by_date[annunciation_date] = (
        annunciation_date,
        readings_by_date.get(annunciation_date, (None, None, None, None, "", None))[1],
        readings_by_date.get(annunciation_date, (None, None, None, None, "", None))[2],
        "",  # Clear meditation
        readings_by_date.get(annunciation_date, (None, None, None, None, "", None))[4],
        "Luke 1:26-38",  # Add NT reading for Annunciation
    )

    readings_by_date[days[1]] = (
        days[1],
        readings_by_date.get(days[1], (None, None, None, None, "", None))[1],
        readings_by_date.get(days[1], (None, None, None, None, "", None))[2],
        "",  # Clear meditation
        "Isaiah 7:10-14",  # Add OT reading for the day before
        readings_by_date.get(days[1], (None, None, None, None, "", None))[5],
    )

    # Reconstruct lexicon
    for date, entry in sorted(readings_by_date.items()):
        adjusted_lexicon.append(entry)

    return adjusted_lexicon

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

    week_number = 0  # Internal week counter for Sundays
    assigned_readings = []

    # Function to convert numbers to ordinals
    def to_ordinal(n):
        if 11 <= n % 100 <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    for i in range(num_days):
        current_date = season_start + timedelta(days=i)
        meditation, ot_reading, nt_reading = "", "", ""

        # Determine the name of the day
        if current_date in named_days.values():
            day_name = [key for key, value in named_days.items() if value == current_date][0]
            # If it's a Sunday, increment the week count for subsequent weekdays
            if current_date.weekday() == 6:
                week_number += 1
        else:
            # For Sundays, increment the week counter and use ordinal for naming
            if current_date.weekday() == 6:  # Sunday
                week_number += 1
                ordinal = to_ordinal(week_number)
                day_name = f"{ordinal} Sunday"
            else:
                # Use the most recent Sunday week number for weekdays
                day_of_week = current_date.strftime("%A")
                day_name = f"{day_of_week} of Week {week_number}"

        # Use readings if provided
        if i < len(daily_readings):
            meditation, ot_reading, nt_reading = daily_readings[i][1:]

        assigned_readings.append(
            (current_date, season_name, day_name, meditation, ot_reading, nt_reading)
        )

    # Handle carry-over readings for the next season
    if carry_over_to is not None and carry_over_readings is not None:
        carry_over_readings.extend(new_carry_over_readings)
    elif carry_over_to is not None:
        carry_over_readings = new_carry_over_readings

    return assigned_readings, carry_over_readings

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

# Main function to generate lexicon CSV
def generate_lexicon_csv(year, readings_file, output_file):
    # Get seasons by calling the liturgical_calendar_markdown function
    _, raw_seasons, celebratory_days = liturgical_calendar_markdown(year)

    # Add reverse flags to the seasons
    seasons = add_reverse_flags(raw_seasons)

    # Load readings from the CSV file
    readings = {}
    with open(readings_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            season = row["SEASON"].strip()
            day = row.get("DAY", "").strip() if row.get("DAY") else ""
            meditation = row.get("Meditation", "").strip() if row.get("Meditation") else ""
            ot_reading = row["OT READING"].strip() if row["OT READING"] else ""
            nt_reading = row["NT YEAR A"].strip() if row["NT YEAR A"] else ""
            if season not in readings:
                readings[season] = []
            readings[season].append((day, meditation, ot_reading, nt_reading))

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

    # Append carry-over readings to Lent
    lent_start = [s for s in seasons if s[0] == "Lent"][0][1]
    for i, (day_name, meditation, nt_reading) in enumerate(carry_over_readings):
        lexicon.append(
            (lent_start + timedelta(days=i), "Lent", day_name, meditation, "", nt_reading)
        )

    # Adjust Annunciation readings
    annunciation_date = celebratory_days[0]["ANNUNCIATION"]
    lexicon = adjust_annunciation_readings(lexicon, annunciation_date)

    # Adjust Harvest readings
    harvest_date = celebratory_days[4]["Harvest"]
    lexicon = adjust_harvest_readings(lexicon, harvest_date)

    # Adjust All Saints readings
    all_saints_date = celebratory_days[0]["ALL SAINTS' DAY"]
    lexicon = adjust_all_saints_readings(lexicon, all_saints_date)

    christ_the_king_date = celebratory_days[2]["Christ the King"]
    lexicon = add_christ_the_king_readings(lexicon, christ_the_king_date)

    # Combine 'Carried Over Days' with existing days where there is no clash
    lexicon = combine_carried_over_readings(lexicon)

    # Write the lexicon to a CSV
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Season", "Day Name", "Meditation", "OT Reading", "NT Reading"])
        for entry in sorted(lexicon, key=lambda x: x[0]):
            writer.writerow(entry)

    print(f"Lexicon CSV saved as {output_file}")

def add_christ_the_king_readings(lexicon, christ_the_king_date):
    """Add specific readings for Christ the King in the OT and NT columns."""
    adjusted_lexicon = []
    readings_by_date = {entry[0]: entry for entry in lexicon}

    # Add the specified readings for Christ the King
    readings_by_date[christ_the_king_date] = (
        christ_the_king_date,
        readings_by_date.get(christ_the_king_date, (christ_the_king_date, "", "", "", "", ""))[1],  # Keep season
        readings_by_date.get(christ_the_king_date, (christ_the_king_date, "", "", "", "", ""))[2],  # Keep day name
        "",
        "Daniel 7:1-14; Psalm 93",  # Add OT readings
        "John 18:28-37; Colossians 1:13-20; Philippians 2:5-11; Revelation 1:4-8",  # Add NT readings
    )

    # Reconstruct the lexicon in sorted order
    for date, entry in sorted(readings_by_date.items()):
        adjusted_lexicon.append(entry)

    return adjusted_lexicon

def adjust_all_saints_readings(lexicon, all_saints_date):
    """
    Adjust readings around All Saints Day:
    - Add specific readings for All Saints Day and the day before.
    - Move all Revelation readings to start 2 days after All Saints if they initially appear on All Saints.
    - Group NT readings around All Saints.
    """
    adjusted_lexicon = []
    readings_by_date = {entry[0]: entry for entry in lexicon}

    print("\nInitial readings by date:")
    for date, entry in sorted(readings_by_date.items()):
        print(f"{date}: {entry}")


    # Step 2: Move all Revelation readings to start 2 days after All Saints if they are on All Saints
    nt_readings = readings_by_date.get(all_saints_date, (None, None, None, None, "", ""))[5]
    print(f"\nNT readings on All Saints Day ({all_saints_date}): {nt_readings}")

    if "Revelation" in nt_readings:
        print("Revelation readings found. Moving all Revelation readings to start 2 days after All Saints.")

        # Collect all dates and NT readings that include Revelation
        revelation_dates = [
            date for date, entry in readings_by_date.items()
            if "Revelation" in entry[5]
        ]
        print(f"Dates with Revelation readings: {revelation_dates}")

        # Collect all Revelation readings in order
        all_revelation_readings = []
        for date in revelation_dates:
            readings = readings_by_date[date][5]
            if "Revelation" in readings:
                all_revelation_readings.extend(readings.split(","))

        print(f"All Revelation readings to move: {all_revelation_readings}")

        # Determine the starting date for Revelation readings (2 days after All Saints)
        start_date = all_saints_date + timedelta(days=2)
        print(f"Revelation readings will start on: {start_date}")

        # Clear existing Revelation readings
        for date in revelation_dates:
            readings_by_date[date] = (
                readings_by_date[date][0],
                readings_by_date[date][1],
                readings_by_date[date][2],
                readings_by_date[date][3],
                readings_by_date[date][4],
                ""  # Clear NT readings
            )

        # Assign Revelation readings starting from the new date
        current_date = start_date
        for reading in all_revelation_readings:
            readings_by_date[current_date] = (
                readings_by_date.get(current_date, (current_date, None, None, None, "", ""))[0],
                readings_by_date.get(current_date, (current_date, None, None, None, "", ""))[1],
                readings_by_date.get(current_date, (current_date, None, None, None, "", ""))[2],
                readings_by_date.get(current_date, (current_date, None, None, None, "", ""))[3],
                readings_by_date.get(current_date, (current_date, None, None, None, "", ""))[4],
                readings_by_date.get(current_date, (current_date, None, None, None, "", ""))[5] + ("," + reading).strip(",")
            )
            current_date += timedelta(days=1)

    else:
        print("No Revelation readings on All Saints Day.")

    # Step 3: Group NT readings around All Saints
    days = [
        all_saints_date - timedelta(days=2),
        all_saints_date - timedelta(days=1),
        all_saints_date,
        all_saints_date + timedelta(days=1),
        all_saints_date + timedelta(days=2),
    ]

    # Collect NT readings for the relevant days
    nt_readings_group = {day: readings_by_date.get(day, (None, None, None, None, "", ""))[5] for day in days}
    print("\nCollected NT readings for relevant days:")
    for day, reading in nt_readings_group.items():
        print(f"{day}: {reading}")

    # Handle the case where All Saints has no NT readings
    if not nt_readings_group[all_saints_date]:
        nt_readings_group[all_saints_date] = ""

    # Split All Saints readings if present
    if nt_readings_group[all_saints_date]:
        chapters = nt_readings_group[all_saints_date].split(",")
        mid = len(chapters) // 2
        above_split = ",".join(chapters[:mid])
        below_split = ",".join(chapters[mid:])
    else:
        above_split = below_split = ""

    # Combine NT readings
    combined_readings_before = nt_readings_group[days[0]]
    if nt_readings_group[days[1]]:
        combined_readings_before = (combined_readings_before + "," + nt_readings_group[days[1]]).strip(",")
    combined_readings_before = (combined_readings_before + "," + above_split).strip(",")

    combined_readings_after = below_split
    if nt_readings_group[days[3]]:
        combined_readings_after = (combined_readings_after + "," + nt_readings_group[days[3]]).strip(",")
    combined_readings_after = (combined_readings_after + "," + nt_readings_group[days[4]]).strip(",")

    print("\nGrouped NT readings:")
    print(f"Before: {combined_readings_before}")
    print(f"After: {combined_readings_after}")

    # Update NT readings in the lexicon
    if combined_readings_before:
        readings_by_date[days[0]] = (
            readings_by_date[days[0]][0],
            readings_by_date[days[0]][1],
            readings_by_date[days[0]][2],
            readings_by_date[days[0]][3],
            readings_by_date[days[0]][4],
            combined_readings_before
        )

    if combined_readings_after:
        readings_by_date[days[4]] = (
            readings_by_date[days[4]][0],
            readings_by_date[days[4]][1],
            readings_by_date[days[4]][2],
            readings_by_date[days[4]][3],
            readings_by_date[days[4]][4],
            combined_readings_after
        )

    # Clear meditations for All Saints and adjacent days
    for day in [days[1], all_saints_date, days[3]]:
        readings_by_date[day] = (
            readings_by_date[day][0],
            readings_by_date[day][1],
            readings_by_date[day][2],
            "",  # Clear meditation
            readings_by_date[day][4],
            ""  # Clear NT readings
        )

    # Step 1: Add specific readings for All Saints Day and the day before
    day_before_all_saints = all_saints_date - timedelta(days=1)

    readings_by_date[day_before_all_saints] = (
        day_before_all_saints,
        readings_by_date.get(day_before_all_saints, (None, "", "", "", "", ""))[1],
        readings_by_date.get(day_before_all_saints, (None, "", "", "", "", ""))[2],
        "",  # Clear meditation
        "Psalm 24; Isaiah 25:1-10",  # OT readings
        ""
    )

    readings_by_date[all_saints_date] = (
        all_saints_date,
        readings_by_date.get(all_saints_date, (None, "", "", "", "", ""))[1],
        readings_by_date.get(all_saints_date, (None, "", "", "", "", ""))[2],
        "",  # Clear meditation
        "",  # No OT readings
        "Matthew 5:3-12; Revelation 7"  # NT readings
    )

    print("\nFinal readings by date:")
    for date, entry in sorted(readings_by_date.items()):
        print(f"{date}: {entry}")

    # Reconstruct lexicon
    for date, entry in sorted(readings_by_date.items()):
        adjusted_lexicon.append(entry)

    return adjusted_lexicon

def adjust_harvest_readings(lexicon, harvest_date):
    """Push all NT readings down by one row to insert Psalm 65 on Harvest."""
    adjusted_lexicon = []
    readings_by_date = {entry[0]: entry for entry in lexicon}

    # Check if Harvest day already has NT readings
    existing_nt_readings = readings_by_date.get(harvest_date, (None, None, None, None, "", ""))[5]

    # Only proceed with shifting if there are existing NT readings
    if existing_nt_readings:
        for date in sorted(readings_by_date.keys(), reverse=True):
            if date > harvest_date:  # Shift only dates after Harvest
                next_date = date + timedelta(days=1)
                readings_by_date[next_date] = readings_by_date[date]

    # Insert Psalm 65 on Harvest day in the OT column
    readings_by_date[harvest_date] = (
        harvest_date,
        readings_by_date.get(harvest_date, (harvest_date, "", "", "", "", ""))[1],  # Keep season
        readings_by_date.get(harvest_date, (harvest_date, "", "", "", "", ""))[2],  # Keep day name
        "",  # Clear meditation
        "Psalm 65",  # Add Psalm 65 to the OT column
        "",  # Clear NT reading
    )

    # Reconstruct the lexicon in sorted order
    for date, entry in sorted(readings_by_date.items()):
        adjusted_lexicon.append(entry)

    return adjusted_lexicon

def ordinal(n):
    """Convert an integer into its ordinal representation."""
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

# Main function to generate lexicon CSV
def main(year):
    year = year
    readings_file = "bible_plan.csv"  # Replace with your readings CSV
    output_file = f"liturgical_calendar_lexicon_{year}.csv"
    generate_lexicon_csv(year, readings_file, output_file)

if __name__ == "__main__":
    main(year)

# John readings should keep going in lent if fot is too short
# for annunciation, harvest, all saints, and christ the king, remove meditations, part readings aside, and add readings

"""
can you modify the script slightly to do the following:

for annunciation, ensure there are no values in the 'Meditations' column for annunciation, the day before, and the day after

also, add the following readings:
- on annuciation, for all NT columns, add luke 1:26-38 as a main reading
- for the day before annunciation, add as an ot reading: Isaiah 7:10-14

then, for harvest, please push all readings down by one row in order to insert Psalm 65. remove the meditation for harvest

for all saints, please do the same grouping thing you've done for annunciation so that the readings around it are grouped backwards and forwards to 2 days before and after if applicable

remove all meditations on all saints, the day before, and the day after

then, for the day before all saints, in the ot readings section add: "Psalm 24; Isaiah 25:1-10", and then, in the nt section, add: "Matthew 5:3-12; Revelation 7"

for christ the king, add these two ot readings: "Daniel 7:1-14;Psalm 93". And for the nt reading: "John 18:28-37; Colossians 1:13-20; Philippians 2:5-11; Revelation 1:4-8" 

please process harvest before processing all saints and christ the king, else the all saints and christ the kings stuff might be messed up
"""
