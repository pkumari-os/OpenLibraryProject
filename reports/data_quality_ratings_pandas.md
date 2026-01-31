# Data Quality Report: Ratings Dataset (Pandas)

## Summary
- **Original row count**: 590,986
- **Cleaned row count**: 590,986
- **Rows removed**: 0 (0.00%)
- **Rows retained**: 100.00%

## Data Quality Metrics

### Rating Year (derived from rating_date)
- **Rows with valid rating_year**: 590,986 (100.00%)
- **Rows with null rating_year**: 0 (0.00%)

### Rating Year Statistics
- **Minimum year**: 2018
- **Maximum year**: 2025

## Schema Changes
- **Added**: `rating_year` (Int16, nullable) - derived from rating_date.year

## Cleaning Steps Applied
1. Removed rows with null or invalid work_key (must start with /works/)
2. Derived rating_year from rating_date for temporal analysis
3. Removed rows with future rating_date
4. Optionally removed rows with rating outside 1-5 (if any)
