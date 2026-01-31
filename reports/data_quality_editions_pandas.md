# Data Quality Report: Editions Dataset (Pandas)

## Summary
- **Original row count**: 55,591,553
- **Cleaned row count**: 53,632,133
- **Rows removed**: 1,959,420 (3.52%)
- **Rows retained**: 96.48%

## Data Quality Metrics

### Publish Year Extraction
- **Rows with valid publish_year**: 52,005,128 (96.97%)
- **Rows with null publish_year**: 1,627,005 (3.03%)

### Publish Year Statistics
- **Minimum year**: 0
- **Maximum year**: 2026
- **Median year**: 2002

## Schema Changes
- **Removed**: `publish_date` (string)
- **Added**: `publish_year` (Int16, nullable)

## Cleaning Steps Applied
1. Extracted year from `publish_date` using regex patterns (same as authors)
2. Validated years (0-2026)
3. Removed rows with null or invalid `work_key` (must start with /works/)
4. Removed rows with null `edition_key`
