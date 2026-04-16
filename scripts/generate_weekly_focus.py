#!/usr/bin/env python3
"""
Generate a weekly quality activity plan.

This script creates a lightweight weekly planning file that complements the
high-frequency automation workflow with one meaningful, review-friendly update.

Usage:
    python scripts/generate_weekly_focus.py
"""

import json
from datetime import datetime
from pathlib import Path

TOPICS_FILE = Path("config/topics.json")
DEFAULT_TOPICS = [
    "AI & Machine Learning",
    "Web Development",
    "Cloud Computing",
    "Data Quality",
    "Open Source Maintenance",
    "Security",
    "System Design",
]

QUALITY_FOCUSES = [
    "Refine repository documentation",
    "Improve test coverage",
    "Reduce workflow risk and noise",
    "Make pull requests easier to review",
    "Improve release-readiness",
    "Increase collaboration signals",
]


def load_topics() -> list[str]:
    """Load topics from config or use defaults."""
    if not TOPICS_FILE.exists():
        return DEFAULT_TOPICS

    try:
        with TOPICS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_TOPICS

    topics = data.get("topics")
    return topics if isinstance(topics, list) and topics else DEFAULT_TOPICS


def build_weekly_content(now: datetime) -> tuple[Path, str]:
    """Build output path and markdown content for the weekly focus file."""
    iso_year, iso_week, _ = now.isocalendar()
    topics = load_topics()
    topic = topics[iso_week % len(topics)]
    focus = QUALITY_FOCUSES[iso_week % len(QUALITY_FOCUSES)]

    folder = Path("updates") / "weekly" / str(iso_year)
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / f"week-{iso_week:02d}.md"
    content = f"""# Weekly Quality Plan - {iso_year}-W{iso_week:02d}

Generated: {now.strftime("%Y-%m-%d %H:%M:%S")}

## Main Focus

- Repository topic: {topic}
- Quality target: {focus}

## Achievement Priorities

- Pull Shark: merge at least one meaningful PR this week
- Pair Extraordinaire: create one co-authored commit that lands in a merged PR
- Quickdraw: reserve one tiny, low-risk PR for fast merge
- YOLO: only use once and only on a very small, obvious change
- Starstruck: improve README or share the project publicly once this week
- Galaxy Brain: answer at least one GitHub Discussion outside this repo
- Public Sponsor: optional external action via GitHub Sponsors

## Suggested Tasks

- [ ] Open one real issue from a template
- [ ] Create one review-friendly PR with a clear summary
- [ ] Improve one document, test, or workflow
- [ ] Record one collaboration action
- [ ] Note one improvement for next week

## Notes

Use this file as the anchor for one weekly quality PR. Keep the daily
automation running, but use this plan to add visible, higher-signal activity.
"""
    return path, content


def main() -> int:
    """Create the weekly plan if it does not already exist."""
    now = datetime.now()
    path, content = build_weekly_content(now)

    if path.exists():
        print(f"Weekly plan already exists: {path}")
        return 0

    path.write_text(content, encoding="utf-8")
    print(f"Created weekly plan: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
