import csv
import datetime
from datetime import timedelta

# Function to calculate Easter
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

# Function to calculate the First Sunday of Advent
def first_sunday_of_advent(year):
    date = datetime.date(year, 11, 27)
    while date.weekday() != 6:  # While it's not Sunday
        date += timedelta(days=1)
    return date

# Function to calculate the day name
def get_day_name(date, season_start):
    delta = (date - season_start).days
    if delta == 0:
        return "First Day of Season"
    elif delta == 1:
        return "Second Day of Season"
    elif delta == 6:
        return "First Sunday of Season"
    elif delta % 7 == 6:
        return f"{(delta // 7) + 1}th Sunday of Season"
    else:
        return f"{delta + 1}th Day of Season"

# Load readings from the CSV file
def load_readings(csv_file):
    readings = {}
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            season = row["SEASON"].strip() if row["SEASON"] else ""
            day = row.get("DAY", "").strip() if row.get("DAY") else ""
            meditation = row.get("Meditation", "").strip() if row.get("Meditation") else ""
            ot_reading = row["OT READING"].strip() if row["OT READING"] else ""
            nt_reading = row.get("NT YEAR A", "").strip() if row.get("NT YEAR A") else ""
            if season not in readings:
                readings[season] = []
            readings[season].append((day, meditation, ot_reading, nt_reading))
    return readings

# Function to adjust readings based on the number of days in the season
def adjust_readings(season, readings, days, reverse=False):
    if len(readings) > days:
        if reverse:  # For Advent, keep later readings
            readings = readings[-days:]
        else:  # For Ordinary Time, keep earlier readings
            readings = readings[:days]
    return readings

# Build the liturgical calendar
def build_liturgical_calendar(year, readings):
    # Calculate key dates
    easter = calculate_easter(year)
    first_advent_sunday = first_sunday_of_advent(year - 1)
    christmas = datetime.date(year - 1, 12, 25)
    epiphany = datetime.date(year, 1, 6)
    ash_wednesday = easter - timedelta(days=46)
    pentecost = easter + timedelta(days=49)
    christ_the_king = first_sunday_of_advent(year) - timedelta(days=7)

    # Calculate season lengths
    advent_days = (christmas - first_advent_sunday).days
    christmas_days = (epiphany - christmas).days
    epiphany_days = 28
    first_ordinary_days = (ash_wednesday - epiphany).days - 1
    lent_days = 46
    easter_days = 50
    second_ordinary_days = (christ_the_king - pentecost).days - 1

    # Adjust readings
    calendar = []
    calendar += assign_readings("Advent", first_advent_sunday, advent_days, readings, reverse=True)
    calendar += assign_readings("Christmas", christmas, christmas_days, readings)
    calendar += assign_readings("Epiphany", epiphany, epiphany_days, readings, baptism_adjust=True)
    calendar += assign_readings("First Ordinary Time", epiphany + timedelta(days=1), first_ordinary_days, readings)
    calendar += assign_readings("Lent", ash_wednesday, lent_days, readings)
    calendar += assign_readings("Easter", easter, easter_days, readings)
    calendar += assign_readings("Second Ordinary Time", pentecost + timedelta(days=1), second_ordinary_days, readings)

    return calendar

# Assign readings to a given season and dates
def assign_readings(season, start_date, num_days, readings, reverse=False, baptism_adjust=False):
    daily_readings = adjust_readings(season, readings.get(season, []), num_days, reverse)
    assigned_readings = []

    for i, (day_name, meditation, ot_reading, nt_reading) in enumerate(daily_readings):
        current_date = start_date + timedelta(days=i)
        day_name = get_day_name(current_date, start_date)
        if baptism_adjust and "Baptism" in day_name:
            # Adjust for baptism readings in Epiphany
            if i == 1:
                assigned_readings[-1] = (assigned_readings[-1][0], assigned_readings[-1][1],
                                         assigned_readings[-1][2], assigned_readings[-1][3], meditation, nt_reading)
            continue
        assigned_readings.append((current_date, season, day_name, meditation, ot_reading, nt_reading))
    return assigned_readings

# Write the calendar to a new CSV file
def write_calendar_to_csv(calendar, output_file):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Season", "Day Name", "Meditation", "OT Reading", "NT Reading"])
        for entry in calendar:
            writer.writerow(entry)

# Main function
def main():
    year = 2025
    readings_file = "bible_plan.csv"
    output_file = f"liturgical_calendar_readings_{year}.csv"

    readings = load_readings(readings_file)
    calendar = build_liturgical_calendar(year, readings)
    write_calendar_to_csv(calendar, output_file)

    print(f"Liturgical calendar with readings saved to {output_file}")

if __name__ == "__main__":
    main()
