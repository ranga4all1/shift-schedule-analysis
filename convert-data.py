import csv
import re
from datetime import datetime, timedelta

# Read the input file
input_file = 'Agent Shifts - Sample.txt'
with open(input_file, 'r') as file:
    data = file.readlines()

# Define a function to parse time strings
def parse_time(time_str):
    try:
        return datetime.strptime(time_str, '%I:%M %p').time()
    except ValueError:
        return datetime.strptime(time_str, '%I %p').time()

# Define a function to parse the shift line and extract relevant information
def parse_shift_line(line):
    match = re.match(r'(Person \d+) (\w+), (\d{2}/\d{2}/\d{4}), (.+): (.+)', line)
    if match:
        person, weekday, date, shift_time, activities = match.groups()
        date = datetime.strptime(date, '%m/%d/%Y').date()
        start_time_str, end_time_str = shift_time.split(' to ')
        start_time = parse_time(start_time_str)
        end_time = parse_time(end_time_str)
        if start_time > end_time:
            end_time = (datetime.combine(date, end_time) + timedelta(days=1)).time()  # Handle midnight crossover
        activities = activities.split(', ')
        return person, weekday, date, start_time, end_time, activities
    elif 'day off' in line.lower():
        match = re.match(r'(Person \d+) (\w+), (\d{2}/\d{2}/\d{4}), (.+)', line)
        if match:
            person, weekday, date, day_off = match.groups()
            date = datetime.strptime(date, '%m/%d/%Y').date()
            return person, weekday, date, None, None, None, day_off
    return None

# Extract the structured data
structured_data = []
for line in data:
    parsed_line = parse_shift_line(line.strip())
    if parsed_line:
        if len(parsed_line) == 7:  # Day off case
            person, weekday, date, _, _, _, day_off = parsed_line
            structured_data.append([date, weekday, person, None, None, None, None, None, day_off])
        else:
            person, weekday, date, start_time, end_time, activities = parsed_line
            prev_activity_end_time = datetime.combine(date, start_time)
            shift_end_time = datetime.combine(date, end_time)
            if shift_end_time < prev_activity_end_time:
                shift_end_time += timedelta(days=1)
            for i, activity in enumerate(activities):
                activity_match = re.match(r'(\w+(?: \w+)?(?: Training)?|Absent) (\d{1,2}(?::\d{2})? [ap]m)', activity)
                if activity_match:
                    activity_type, activity_time = activity_match.groups()
                    activity_start_time = datetime.combine(date, parse_time(activity_time))
                    if activity_start_time < prev_activity_end_time:
                        activity_start_time += timedelta(days=1)
                    # Determine the end time of the current activity
                    if i + 1 < len(activities):
                        next_activity_match = re.match(r'.+ (\d{1,2}(?::\d{2})? [ap]m)', activities[i + 1])
                        if next_activity_match:
                            next_activity_time = parse_time(next_activity_match.group(1))
                            activity_end_time = datetime.combine(date, next_activity_time)
                            if activity_end_time < activity_start_time:
                                activity_end_time += timedelta(days=1)
                        else:
                            activity_end_time = shift_end_time
                    else:
                        activity_end_time = shift_end_time

                    structured_data.append([
                        date, weekday, person, start_time, end_time, activity_type,
                        prev_activity_end_time.time(), activity_end_time.time(), None
                    ])
                    prev_activity_end_time = activity_end_time

# Write the structured data to a CSV file
output_file = 'Agent_Shifts_Structured.csv'
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['Date', 'Weekday', 'Person', 'Shift Start Time', 'Shift End Time', 'Activity', 'Activity Start Time', 'Activity End Time', 'Day Off']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in structured_data:
        writer.writerow({
            'Date': row[0],
            'Weekday': row[1],
            'Person': row[2],
            'Shift Start Time': row[3],
            'Shift End Time': row[4],
            'Activity': row[5],
            'Activity Start Time': row[6],
            'Activity End Time': row[7],
            'Day Off': row[8],
        })

print(f"Structured data has been written to {output_file}")
