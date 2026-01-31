# Data Quality Report: Works Dataset (Pandas)

## Summary
- **Original row count**: 40,688,965
- **Cleaned row count**: 40,688,902
- **Rows removed**: 63 (0.00%)
- **Rows retained**: 100.00%

## Data Quality Metrics
- **Rows with non-null title**: 40,688,902
- **Rows with non-null author_key**: 38,458,493
- **Rows with non-null subjects**: 19,854,712

## Schema (unchanged)
- work_key (String, required)
- title (String, required)
- author_key (String, nullable)
- subjects (List[String], nullable)

## Cleaning Steps Applied
1. Removed rows with null or invalid work_key (must start with /works/)
2. Trimmed whitespace from title; removed rows with null/empty title
3. Cleaned author_key: strip; set invalid or empty to null
4. Cleaned subjects: trim items, empty list → null, limit to first 5 items
