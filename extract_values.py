import csv
import re

# Input and output files
TXT_FILE = "values.txt"
CSV_FILE = "person_solutions_prod_2.csv"

# Read the SQL file
with open(TXT_FILE, "r", encoding="utf-8") as file:
    content = file.read()

# Extract tuples inside VALUES(...)
# Matches things like: (1,1,371,3,5)
matches = re.findall(r"\((.*?)\)", content)

rows = []
for match in matches:
    # Split values by comma and remove spaces
    values = [v.strip() for v in match.split(",")]

    # Expect exactly 5 values: id, solutionState, person, solution, organization
    if len(values) == 5:
        rows.append(values)
    else:
        print(f"⚠️ Skipping malformed row: {match}")

# Write to CSV file
with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "solutionState", "person", "solution", "organization"])  # header
    writer.writerows(rows)

print(f"✅ Extracted {len(rows)} rows into {CSV_FILE}")
