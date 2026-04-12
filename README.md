# Auto Contributions

Automation-first repository for building steady GitHub activity while keeping a cleaner, more review-friendly workflow.

## What This Repo Does

- Creates scheduled daily contribution updates under `updates/YYYY/MM/`.
- Keeps a separate weekly quality layer for calmer, higher-signal pull requests.
- Supports achievement-focused workflows such as `Pull Shark`, `Quickdraw`, and `Pair Extraordinaire`.
- Provides helper scripts for merge management, conflict resolution, and status reporting.

## Active Workflow Priority

1. `code-quality.yml`
   Quality gate for formatting and linting.
2. `daily-contribution.yml`
   Creates the scheduled daily update PR.
3. `auto-merge.yml`
   Resolves stale branches and merges eligible daily PRs.
4. `weekly-quality.yml`
   Creates one slower, more review-friendly weekly planning PR.

## Repository Structure

```text
Auto/
|-- .github/
|   |-- workflows/
|   `-- ISSUE_TEMPLATE/
|-- config/
|-- docs/
|   |-- guides/
|   `-- archive/
|-- scripts/
|-- tests/
|-- updates/
|-- CHANGELOG.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- README.md
`-- SECURITY.md
```

## Main Commands

```bash
# Generate one local daily update
python generate_content.py

# Check PR system health
python scripts/pr_status_report.py

# Resolve stale or conflicted PR branches
python scripts/resolve_conflicts.py --auto-resolve

# Review and merge ready PRs manually
python scripts/review_and_merge_prs.py --auto-merge

# Validate local installation
python scripts/validate_installation.py
```

## Documentation

- Active guides index: [docs/README.md](./docs/README.md)
- Achievement strategy: [docs/guides/GITHUB_ACHIEVEMENTS_HYBRID_PLAN_FA.md](./docs/guides/GITHUB_ACHIEVEMENTS_HYBRID_PLAN_FA.md)
- Quick start: [docs/guides/QUICKSTART.md](./docs/guides/QUICKSTART.md)
- Merge guide: [docs/guides/MERGE_PRS_GUIDE.md](./docs/guides/MERGE_PRS_GUIDE.md)
- Conflict resolution: [docs/guides/CONFLICT_RESOLUTION_GUIDE.md](./docs/guides/CONFLICT_RESOLUTION_GUIDE.md)
- Collaboration guides: [docs/guides/HOW_TO_INVITE_FRIENDS.md](./docs/guides/HOW_TO_INVITE_FRIENDS.md)

## Notes

- Scheduled daily runs no longer update `README.md`, which reduces merge conflicts and PR backlog.
- High-volume helper scripts are still available, but they are now manual-only and not part of the normal scheduled path.
- Historical summaries and one-off implementation reports were moved out of the root into `docs/archive/`.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).
