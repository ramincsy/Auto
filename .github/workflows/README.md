# Workflow Priority

## Active Workflows

1. `code-quality.yml`
2. `daily-contribution.yml`
3. `auto-merge.yml`
4. `weekly-quality.yml`

## Rationale

- `code-quality.yml` protects the repository baseline.
- `daily-contribution.yml` creates scheduled contribution PRs.
- `auto-merge.yml` resolves stale branches and processes eligible daily PRs.
- `weekly-quality.yml` adds one calmer, review-friendly quality PR each week.

## Cleanup Notes

- The older `complete-contribution.yml` workflow was removed because it created too much noise and too many worker-style actions for the default repository path.
- Bulk helper scripts remain available, but only through manual execution outside the default Actions path.
- The daily workflow now only creates the main scheduled PR and no longer runs bulk helper steps or best-effort pre-commit checks.
- The active workflows now declare explicit permissions, concurrency groups, and timeouts to keep runs more predictable.
