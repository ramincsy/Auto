# Changelog

All notable changes to this project are documented here.

## [1.3.0] - Unreleased

### Changed
- Cleaned the repository root and moved non-core markdown files into `docs/`.
- Split documentation into active guides and archived reports.
- Removed the high-volume `complete-contribution` workflow from the active repository layout.
- Simplified the scheduled daily workflow so it no longer edits `README.md`.
- Kept bulk helper scripts as manual tools instead of scheduled workers.

### Added
- `docs/README.md` as the documentation index.
- `scripts/README.md` as the script inventory and priority guide.
- `.github/workflows/README.md` as the workflow priority and maintenance guide.
- `tests/` directory for local validation scripts.

### Removed
- Unused high-volume worker files from active workflow usage.
- Temporary local contribution test files created during validation.

## [1.2.0] - Unreleased

### Added
- Hybrid achievements strategy document in `docs/guides/GITHUB_ACHIEVEMENTS_HYBRID_PLAN_FA.md`
- Repository metadata files: `LICENSE`, `CODEOWNERS`, PR template, and Issue templates
- Weekly quality planning script: `scripts/generate_weekly_focus.py`
- Weekly quality workflow: `.github/workflows/weekly-quality.yml`

### Changed
- README now explains the hybrid model for GitHub Achievements
- Repository guidance now distinguishes active, limited, and historical badges

## [1.0.0] - 2025-12-13

### Added
- Automated daily contributions
- Daily update files under `updates/YYYY/MM/`
- Core contribution scripts and setup files
- Pre-commit based formatting and linting
- Initial documentation set
