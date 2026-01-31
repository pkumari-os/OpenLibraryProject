# Overall Rank Table — Report

## Purpose
This table feeds the **long tail of popularity** analysis. Each row is one work (book) with a combined **popularity_score** and **overall_rank**.

## Output file
- **Path**: data/processed/overall_rank.parquet
- **Rows**: 3,000,008

## Columns
| Column | Description |
|--------|-------------|
| work_key | Unique work identifier (e.g. /works/OL123W) |
| count_of_ratings | Number of ratings for this work |
| bayesian_rating | Bayesian average rating (prior-pulled when few ratings) |
| average_rating | Simple average rating |
| want_to_read | Count of "want to read" in reading log |
| already_read | Count of "already read" in reading log |
| currently_reading | Count of "currently reading" in reading log |
| popularity_score | Combined score (see formula) |
| overall_rank | Rank by popularity_score (1 = highest) |

## Popularity score formula
**popularity_score** = 1 × (bayesian_rating) + 0.8 × (already_read) + 0.4 × (currently_reading) + 0.1 × (want_to_read)

Values are stored with 10 decimal places for fine rank comparison.

## Summary statistics
- popularity_score — min: 0.1000000000, max: 8086.2852073843, mean: 1.0779844402
- overall_rank — 1 to 1,383,682
- count_of_ratings — max: 1,275
- already_read — max: 1,527
