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
| title | Work title from works_cleaned (null if not in works) |
| count_of_ratings | Number of ratings for this work |
| bayesian_rating | Bayesian average rating (prior-pulled when few ratings) |
| average_rating | Simple average rating |
| want_to_read | Count of "want to read" in reading log |
| already_read | Count of "already read" in reading log |
| currently_reading | Count of "currently reading" in reading log |
| norm_log_bayesian_rating | Norm(log(1 + bayesian_rating)) in [0, 1] |
| norm_log_already_read | Norm(log(1 + already_read)) in [0, 1] |
| norm_log_want_to_read | Norm(log(1 + want_to_read)) in [0, 1] |
| norm_log_currently_reading | Norm(log(1 + currently_reading)) in [0, 1] |
| popularity_score | Combined score (see formula) |
| overall_rank | Rank by popularity_score (1 = highest) |

## Popularity score formula
1. Log-scale: log(1 + value) per metric. 2. Normalize to 0–1: Norm(x) = (x − min) / (max − min) per metric.  
**popularity_score** = 1 × Norm(log(bayesian_rating)) + 0.8 × Norm(log(already_read)) + 0.4 × Norm(log(currently_reading)) + 0.1 × Norm(log(want_to_read))

Values are stored with 10 decimal places for fine rank comparison.

## Summary statistics
- popularity_score — min: 0.0063914575, max: 2.9127945851, mean: 0.1216964416
- overall_rank — 1 to 1,383,682
- count_of_ratings — max: 1,275
- already_read — max: 1,527
