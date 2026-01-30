# Data Quality Report: Authors Dataset (Pandas)

## Summary
- **Original row count**: 14,970,140
- **Cleaned row count**: 14,967,825
- **Rows removed**: 2,315 (0.02%)
- **Rows retained**: 99.98%

## Data Quality Metrics

### Birth Year Extraction
- **Rows with valid birth_year**: 1,899,075 (12.69%)
- **Rows with null birth_year**: 13,068,750 (87.31%)

### Birth Year Statistics
- **Minimum year**: 4
- **Maximum year**: 2025
- **Median year**: 1928
- **Mean year**: 1904

## Schema Changes
- **Removed**: `birth_date` (string, various formats)
- **Added**: `birth_year` (Int16, standardized year)

## Cleaning Steps Applied
1. Extracted year from `birth_date` using regex patterns
2. Validated years (range: 0-2026)
3. Trimmed whitespace from `name` field
4. Removed rows with null/empty `author_key` or `name`

## Tools Used
- **Library**: Pandas
- **Date Extraction**: Custom regex-based function
- **Output Format**: Parquet (columnar, compressed)
