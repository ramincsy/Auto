import os
import random
import json
from datetime import datetime
from pathlib import Path

# Load topic configuration
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
]


def load_topics():
    """Load topics from config file or use defaults."""
    if Path(TOPICS_FILE).exists():
        try:
            with open(TOPICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("topics", DEFAULT_TOPICS)
        except Exception:
            return DEFAULT_TOPICS
    return DEFAULT_TOPICS


def get_topic_for_date(date_str, topics):
    """Select topic based on date to avoid repetition within a week."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        week_offset = date_obj.isocalendar()[1] % len(topics)
        return topics[week_offset]
    except Exception:
        return random.choice(topics)


def generate_content(date_str=None):
    """Generate daily content with topic rotation."""
    topics = load_topics()
    if date_str:
        topic = get_topic_for_date(date_str, topics)
    else:
        topic = random.choice(topics)
    return f"📚 Studied: {topic}"


def get_date_string():
    """Get date string from env or system date."""
    year = os.getenv("year")
    month = os.getenv("month")
    day = os.getenv("day")
    if not (year and month and day):
        today = datetime.today()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = today.strftime("%d")
    return f"{year}-{month}-{day}"


def ensure_daily_entry():
    """Append daily section to README once per day."""
    date_string = get_date_string()
    readme_header = f"## 📅 {date_string}\n"

    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        content = "# 🚀 Auto Contributions\n\n"

    if readme_header not in content:
        with open("README.md", "a", encoding="utf-8") as f:
            f.write("\n")
            f.write(readme_header)
            for i in range(3):
                content_line = generate_content(date_string)
                f.write(f"- {content_line}\n")


def write_update_file():
    """Create updates/YYYY/MM/DD.md with daily summary."""
    date_string = get_date_string()
    parts = date_string.split("-")
    year, month, day = parts[0], parts[1], parts[2]

    folder = Path("updates") / year / month
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / f"{day}.md"
    if not path.exists():
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# Daily Update - {date_string}\n\n")
            f.write("## 📝 Summary\n")
            f.write(f"Contributed on {date_string}.\n\n")
            f.write("## 🎯 Topics Studied\n")
            topics = load_topics()
            topic = get_topic_for_date(date_string, topics)
            f.write(f"- {topic}\n")
            f.write("\n## 📌 Notes\n")
            f.write("Add your daily notes here.\n")


def main():
    """Main function to generate daily content."""
    ensure_daily_entry()
    write_update_file()
    print(f"✅ Daily contribution recorded for {get_date_string()}")


if __name__ == "__main__":
    main()
