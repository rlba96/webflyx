import csv
import requests
import urllib3

# Disable SSL warnings (since it's a local HTTPS endpoint)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Path to your CSV file
CSV_FILE = "person_solutions_prod.csv"

# Base URL and Authorization header
BASE_URL = "https://192.168.10.149:8443/persons/solutions/update_orgs"
HEADERS = {
    "Authorization": "OneCare eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzdXBlcmFkbWluIiwiZXhwIjoxNzYzNTYyNzc5fQ.J8qN3u1O7VmYlx7dVrvYX0-lXOmEuNd9j9MQXOzwdiDa7MOJaLLJVDSSFMaakIWtzQ5YhPKBD7nm9TRMZUt8oA"
}

def update_orgs_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        print(f"Header columns: {header}")

        # Automatically detect relevant columns
        id_index = None
        org_index = None
        for i, col in enumerate(header):
            col_lower = col.lower()
            if "personsolution" in col_lower or (col_lower == "id"):
                id_index = i
            elif "org" in col_lower or "organization" in col_lower:
                org_index = i

        if id_index is None or org_index is None:
            print("❌ Could not find both 'personSolution' and 'organization' columns in CSV.")
            return

        for row in reader:
            person_solution_id = row[id_index].strip()
            org_id = row[org_index].strip()

            if not person_solution_id:
                continue  # skip invalid rows

            # url = f"{BASE_URL}?personSolution={person_solution_id}&orgId={org_id if org_id else 'null'}"
            # fromId
            # toId
            url = f"{BASE_URL}?personSolution={person_solution_id}&ignoreFilled=true&fromId=3501&toId=4006"
            print(f"➡️ Sending request: {url}")

            try:
                response = requests.get(url, headers=HEADERS, verify=False)
                print(f"✅ ID {person_solution_id} -> {response.status_code}: {response.text[:100]}")
            except Exception as e:
                print(f"⚠️ Failed for ID {person_solution_id}: {e}")

if __name__ == "__main__":
    update_orgs_from_csv(CSV_FILE)
