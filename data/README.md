# Local NFL Big Data Bowl 2025 data

Download the official dataset from:
https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/data

Sign in and accept the competition rules on Kaggle before downloading. Extract the archive into this directory so `games.csv`, `plays.csv`, `players.csv`, `player_play.csv`, and `tracking_week_*.csv` are directly under `data/`.

If the official Kaggle CLI is installed and authenticated:

```sh
kaggle competitions download -c nfl-big-data-bowl-2025 -p data
unzip -n data/nfl-big-data-bowl-2025.zip -d data
```

All files in this directory except this README are ignored by Git, including archives and derived records. Do not commit credentials. Data remains subject to the competition rules.

Download status on October 8, 2026: after sign-in and competition-rule acceptance, Kaggle reports: "The dataset for this competition has been removed at the request of the host." The official CSV archive is unavailable; no dataset files were downloaded. An authorized existing copy or an alternative dataset is needed.

## Available replacement: regional-event release

Source: https://github.com/ThompsonJamesBliss/nfl-big-data-bowl-regional-event-data

The publisher documents NFL Next Gen Stats tracking and PFF scouting/coverage labels. This release is separate from Big Data Bowl 2025 and contains 8,557 plays from 122 games in weeks 1–8 of the 2021 season, with 12 distinct `pff_passCoverage` labels.

Local location: `data/regional-2021/`. Tracking is split into `tracking/tracking_<gameId>.csv`, alongside `games.csv`, `plays.csv`, `players.csv`, and `pffScoutingData.csv`. Unlike the 2025 schema, tracking uses `team` rather than `club` and does not have `frameType`; use `frameId` strictly below the play's `ball_snap` event. The related annotation is `pff_passCoverageType`, not `pff_manZone`. Do not include either coverage field as a predictor.

The ignored `manifest.json` records the source revision, byte sizes and SHA-256 hashes. The ignored `audit.json` records complete pre-snap snapshot counts and three actual source examples. All downloaded and derived records remain local.

Verified local audit: 122 tracking files, 8,314,178 tracking rows, and 8,522 labeled plays with a complete strictly pre-snap snapshot containing 11 distinct players per team. The remaining 35 plays did not satisfy these initial snapshot checks. This audit does not establish annotation accuracy or the suitability of every rare coverage class.

To reproduce the audit from the repository root, use:

```sh
uv run --with pandas python scripts/audit_regional_data.py
```
