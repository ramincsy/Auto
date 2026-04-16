#!/usr/bin/env python3
"""
Generate multiple contribution files for an optional manual bulk run.

Usage:
    python scripts/generate_multiple_contributions.py [count]

Default:
    Uses BULK_COUNT if set, otherwise 20 contributions per execution
"""

import os
import random
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

TOPICS_FILE = "config/topics.json"
DEFAULT_TOPICS = [
    "AI",
    "Machine Learning",
    "Data Science",
    "Web Development",
    "Cloud Computing",
    "DevOps",
    "Security",
    "Open Source",
    "Mobile Development",
    "Blockchain",
    "IoT",
    "Cybersecurity",
]


def load_topics():
    """Load topics from config file."""
    if Path(TOPICS_FILE).exists():
        try:
            with open(TOPICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("topics", DEFAULT_TOPICS)
        except Exception:
            return DEFAULT_TOPICS
    return DEFAULT_TOPICS


def get_random_topic(topics):
    """Get a random topic."""
    return random.choice(topics)


def generate_contribution_file(date_str, index, topics):
    """
    Generate a single contribution file.

    Args:
        date_str: Date in YYYY-MM-DD or YYYY-MM-DD-HH format
        index: Contribution index (0-4)
        topics: List of topics

    Returns:
        Path to created file
    """
    parts = date_str.split("-")
    year, month, day = parts[0], parts[1], parts[2]
    hour = parts[3] if len(parts) > 3 else None

    folder = Path("updates") / year / month
    folder.mkdir(parents=True, exist_ok=True)

    # Create unique filename for each contribution
    filename = f"{day}-contribution-{index}.md"
    if hour:
        filename = f"{day}-{hour}-contribution-{index}.md"
    filepath = folder / filename

    if filepath.exists():
        return None  # Skip if already exists

    topic = get_random_topic(topics)
    timestamp = datetime.now().isoformat()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Contribution #{index} - {date_str}\n\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        f.write("## 📚 Topic Studied\n")
        f.write(f"- {topic}\n\n")
        f.write("## 🎯 Activity\n")
        f.write(f"- Random contribution #{index}\n")
        f.write("- Part of automated contribution system\n")
        f.write(f"- Date: {date_str}\n\n")
        f.write("## 📝 Details\n")
        f.write(f"- Index: {index}\n")
        f.write(f"- Topic: {topic}\n")
        f.write(f"- Generated: {timestamp}\n")

    return filepath


def update_readme(date_str, count):
    """Add contribution summary to README."""
    # Skip README update to avoid git conflicts
    # README updates are handled separately by main daily workflow
    pass


def get_date_string():
    """Get date string from environment or system.

    Includes hour/minute/second if available to make multiple same-day runs unique.
    """
    year = os.getenv("year")
    month = os.getenv("month")
    day = os.getenv("day")
    hour = os.getenv("hour")
    minute = os.getenv("minute")
    second = os.getenv("second")

    if not (year and month and day):
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")

    if hour:
        result = f"{year}-{month}-{day}-{hour}"
        if minute:
            result += f"-{minute}"
        if second:
            result += f"-{second}"
        return result
    return f"{year}-{month}-{day}"


def get_bulk_count() -> int:
    """Return the requested contribution count."""
    raw_value = sys.argv[1] if len(sys.argv) > 1 else os.getenv("BULK_COUNT", "20")
    try:
        count = int(raw_value)
    except ValueError:
        count = 20

    return max(2, min(count, 100))


def main():
    """Generate multiple contributions."""
    count = get_bulk_count()

    date_string = get_date_string()
    topics = load_topics()

    print(f"📊 Generating {count} contributions for {date_string}...")

    created_count = 0
    for i in range(count):
        filepath = generate_contribution_file(date_string, i, topics)
        if filepath:
            print(f"  ✅ Created: {filepath}")
            created_count += 1
        else:
            print(f"  ⏭️  Skipped (already exists): contribution-{i}")

    if created_count > 0:
        update_readme(date_string, created_count)
        print(f"\n✨ Successfully created {created_count} contribution files!")
    else:
        print(f"\n⚠️  No new contributions created (all already exist)")

    return created_count


if __name__ == "__main__":
    created = main()
    sys.exit(0)  # Always exit successfully to avoid blocking workflow
