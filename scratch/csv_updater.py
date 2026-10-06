import csv, sys, json

CSV_PATH = r"E:\Extra\job-kit-starter\job-kit-starter\output\job-search\applications.csv"

def append_row(data):
    today = "2026-09-24"
    fieldnames = [
        "Company", "Role", "Location", "Channel", "Comp", "Status",
        "Added", "Applied", "Updated", "Resume", "Job URL", "Next step", "Personal Info Filled"
    ]
    status = data.get("Status", "Lead")
    row = {
        "Company": data.get("Company", ""),
        "Role": data.get("Role", ""),
        "Location": data.get("Location", ""),
        "Channel": data.get("Channel", ""),
        "Comp": data.get("Comp", ""),
        "Status": status,
        "Added": data.get("Added", today),
        "Applied": today if status == "Applied" else "",
        "Updated": today,
        "Resume": data.get("Resume", ""),
        "Job URL": data.get("Job URL", ""),
        "Next step": data.get("Next step", ""),
        "Personal Info Filled": data.get("Personal Info Filled", "")
    }
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)
    print(f"Logged {row['Company']} - {row['Role']} as {row['Status']}")

if __name__ == "__main__":
    raw = sys.argv[1]
    data = json.loads(raw)
    append_row(data)
