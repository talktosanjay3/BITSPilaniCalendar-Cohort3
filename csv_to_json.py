#!/usr/bin/env python3
"""Convert WeekCompo.csv to schedule.json.

Usage:
    python csv_to_json.py                    # uses default paths
    python csv_to_json.py input.csv          # custom input
    python csv_to_json.py input.csv out.json # custom input + output

The output JSON is formatted for easy manual editing.
"""

import csv
import json
import sys
from datetime import datetime


def parse_component(component: str) -> str:
    """Map CSV component to JSON type."""
    if "LIVE CLASS" in component:
        return "live"
    if "QUIZ" in component:
        return "quiz"
    if "ASSIGNMENT" in component:
        return "assignment"
    if "EXAM" in component:
        return "exam"
    return "info"


def csv_to_schedule(csv_path: str = "WeekCompo.csv") -> dict:
    """Read CSV and return schedule dict."""
    events = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            week = int(row["Week"].strip())
            component = row["Component"].strip()
            start_date = row["Start Date"].strip()
            end_date = row["End Date"].strip()
            start_time = row["Start Time (IST)"].strip() or None
            end_time = row["End Time (IST)"].strip() or None
            course = row["Course"].strip() or None
            weightage_str = row["Weightage"].strip()
            weightage = int(weightage_str) if weightage_str else None

            event = {
                "week": week,
                "component": component,
                "date": start_date,
                "startTime": start_time,
                "endTime": end_time,
                "course": course,
                "weightage": weightage,
                "type": parse_component(component),
            }

            # Multi-day events get endDate
            if start_date and end_date and start_date != end_date:
                event["endDate"] = end_date

            events.append(event)

    schedule = {
        "metadata": {
            "title": "BITS Pilani — MSc DS & AI",
            "cohort": "Cohort 3",
            "trimester": 2026,
            "timezone": "IST",
            "source": "Trimester calendar",
        },
        "events": events,
    }

    return schedule


def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "WeekCompo.csv"
    json_path = sys.argv[2] if len(sys.argv) > 2 else "schedule.json"

    print(f"Reading {csv_path}...")
    schedule = csv_to_schedule(csv_path)

    print(f"Writing {json_path}...")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total = len(schedule["events"])
    weeks = sorted(set(e["week"] for e in schedule["events"]))
    print(f"Done! {total} events across weeks {min(weeks)}–{max(weeks)}")


if __name__ == "__main__":
    main()
