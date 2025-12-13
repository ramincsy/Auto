#!/usr/bin/env python3
"""
CLI tool for logging daily contributions and notes.

Usage:
  python scripts/log_daily.py --note "Your daily note here"
  python scripts/log_daily.py --topic "Custom Topic"
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def log_note(note: str):
    """Add a note to today's update file."""
    today = datetime.now()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    date_str = f"{year}-{month}-{day}"

    folder = Path("updates") / year / month
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{day}.md"

    if not path.exists():
        path.write_text(f"# Daily Update - {date_str}\n\n", encoding="utf-8")

    content = path.read_text(encoding="utf-8")

    if "## 📌 Notes" not in content:
        content += "\n## 📌 Notes\n"

    content += f"- {note}\n"
    path.write_text(content, encoding="utf-8")
    print(f"✅ Note added to {path}")


def update_topic(topic: str):
    """Update topic for today."""
    today = datetime.now()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    date_str = f"{year}-{month}-{day}"

    folder = Path("updates") / year / month
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{day}.md"

    if not path.exists():
        path.write_text(f"# Daily Update - {date_str}\n\n", encoding="utf-8")

    content = path.read_text(encoding="utf-8")

    if "## 🎯 Topics Studied" not in content:
        content += "\n## 🎯 Topics Studied\n"
        content += f"- {topic}\n"
    else:
        # Append to existing topics
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line == "## 🎯 Topics Studied":
                # Find insertion point
                j = i + 1
                while j < len(lines) and lines[j].startswith("- "):
                    j += 1
                lines.insert(j, f"- {topic}")
                content = "\n".join(lines)
                break

    path.write_text(content, encoding="utf-8")
    print(f"✅ Topic '{topic}' recorded in {path}")


def main():
    parser = argparse.ArgumentParser(description="Log daily contributions")
    parser.add_argument("--note", type=str, help="Add a note to today's update")
    parser.add_argument("--topic", type=str, help="Record a topic studied")
    parser.add_argument("--list", action="store_true", help="List all topics")

    args = parser.parse_args()

    if args.note:
        log_note(args.note)
    elif args.topic:
        update_topic(args.topic)
    elif args.list:
        config_path = Path("config/topics.json")
        if config_path.exists():
            data = json.loads(config_path.read_text())
            print("\n📚 Available Topics:")
            for topic in data.get("topics", []):
                print(f"  - {topic}")
        else:
            print("Config file not found")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
