
import polars as pl
from pathlib import Path
import json

# Import the new schemas
from work_schema import WORK_SCHEMA
from edition_schema import EDITION_SCHEMA
from author_schema import AUTHOR_SCHEMA

# Configuration
DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(exist_ok=True, parents=True)

def process_works():
    """
    Process Works Dump: Extracts Title and Subjects.
    Input: TSV | Columns: type, key, rev, last_mod, json
    """
    print("Processing Works dump...")
    input_path = RAW_DIR / "ol_dump_works_2025-12-31.txt"
    output_path = PROCESSED_DIR / "works.parquet"
    
    if not input_path.exists():
        print(f"Skipping {input_path} (not found)")
        return

    # Scan CSV lazily (doesn't load into RAM)
    q = (
        pl.scan_csv(
            input_path, 
            separator="\t", 
            has_header=False, 
            new_columns=["type", "key", "revision", "last_modified", "json_blob"],
            quote_char=None, # Disable quoting to speed up and avoid issues with unescaped quotes
            ignore_errors=True # Skip malformed lines
        )
        .select([
            pl.col("key").alias("work_key"),
            # Extract basic fields from JSON using the defined schema
            pl.col("json_blob").str.json_decode(WORK_SCHEMA).alias("json"),
        ])
        .select([
            pl.col("work_key"),
            pl.col("json").struct.field("title"),
            # Extract top 5 subjects as a list (for genre analysis)
            pl.col("json").struct.field("subjects").list.slice(0, 5).fill_null([]),
        ])
    )
    
    # Streaming write to Parquet (chunks processing automatically)
    q.sink_parquet(output_path)
    print(f"Saved to {output_path}")


def process_editions():
    """
    Process Editions Dump: Extracts Publish Date and Work Links.
    """
    print("Processing Editions dump...")
    input_path = RAW_DIR / "ol_dump_editions_2025-12-31.txt"
    output_path = PROCESSED_DIR / "editions.parquet"
    
    if not input_path.exists():
        print(f"Skipping {input_path} (not found)")
        return

    q = (
        pl.scan_csv(
            input_path, 
            separator="\t", 
            has_header=False, 
            new_columns=["type", "key", "revision", "last_modified", "json_blob"],
            quote_char=None,
            ignore_errors=True
        )
        .select([
            pl.col("key").alias("edition_key"),
            pl.col("json_blob").str.json_decode(EDITION_SCHEMA).alias("json")
        ])
        .select([
            pl.col("edition_key"),
            # Extract Publish Date (Critical for timeline)
            pl.col("json").struct.field("publish_date"),
            # Link to Work Key (needed to join with Ratings/Works)
            # data structure: works: [{key: /works/OL...}]
            pl.col("json")
                .struct.field("works")
                .list.first()
                .struct.field("key")
                .alias("work_key")
        ])
    )
    q.sink_parquet(output_path)
    print(f"Saved to {output_path}")


def process_authors():
    """
    Process Authors Dump: Extracts Name and Birth Date.
    """
    print("Processing Authors dump...")
    input_path = RAW_DIR / "ol_dump_authors_2025-12-31.txt"
    output_path = PROCESSED_DIR / "authors.parquet"
    
    if not input_path.exists():
        print(f"Skipping {input_path} (not found)")
        return

    q = (
        pl.scan_csv(
            input_path, 
            separator="\t", 
            has_header=False, 
            new_columns=["type", "key", "revision", "last_modified", "json_blob"],
            quote_char=None,
            ignore_errors=True
        )
        .select([
            pl.col("key").alias("author_key"),
            pl.col("json_blob").str.json_decode(AUTHOR_SCHEMA).alias("json")
        ])
        .select([
            pl.col("author_key"),
            pl.col("json").struct.field("name"),
            pl.col("json").struct.field("birth_date"),
        ])
    )
    q.sink_parquet(output_path)
    print(f"Saved to {output_path}")


def process_ratings():
    """
    Process Ratings Dump: Jagged TSV (Work, [Edition], Rating, Date).
    Format: work_key \t [edition_key \t] rating \t date
    """
    print("Processing Ratings dump...")
    input_path = RAW_DIR / "ol_dump_ratings_2025-12-31.txt"
    output_path = PROCESSED_DIR / "ratings.parquet"
    
    if not input_path.exists():
        print(f"Skipping {input_path} (not found)")
        return

    # Handle jagged structure: 3 or 4 columns
    # Format: work_key \t [edition_key \t] rating \t date
    q = (
        pl.scan_csv(
            input_path,
            has_header=False,
            new_columns=["raw_line"],
            separator="\n", # Read full line
            quote_char=None
        )
        .with_columns(
            pl.col("raw_line").str.split("\t").alias("parts")
        )
        .select([
            pl.col("parts").list.get(0).alias("work_key"),
            
            # Logic: If len == 4, index 1 is Edition. If len == 3, Edition is Null.
            pl.when(pl.col("parts").list.len() == 4)
              .then(pl.col("parts").list.get(1))
              .otherwise(pl.lit(None))
              .alias("edition_key"),
              
            # Logic: If len == 4, index 2 is Rating. If len == 3, index 1 is Rating.
            pl.when(pl.col("parts").list.len() == 4)
              .then(pl.col("parts").list.get(2))
              .otherwise(pl.col("parts").list.get(1))
              .alias("rating"),
              
            # Logic: Last column is always Date
            pl.col("parts").list.last().alias("rating_date")
        ])
        .with_columns([
            # Convert rating to integer
            pl.col("rating").cast(pl.Int8),
            # Parse date with explicit format (YYYY-MM-DD)
            pl.col("rating_date").str.to_date(format="%Y-%m-%d", strict=False)
        ])
    )
    
    q.sink_parquet(output_path)
    print(f"Saved to {output_path}")


def process_reading_log():
    """
    Process Reading Log: Jagged TSV (Work, [Edition], Status, Date).
    We use a schema hack: Read line as single string, then split manually to handle optional column.
    """
    print("Processing Reading Log dump...")
    input_path = RAW_DIR / "ol_dump_reading-log_2025-12-31.txt"
    output_path = PROCESSED_DIR / "reading_log.parquet"
    
    if not input_path.exists():
        print(f"Skipping {input_path} (not found)")
        return

    # Optimization: Loading as single text line because of jagged columns (3 or 4 cols)
    # This is slightly slower but safer for jagged data
    # format: Work \t [Edition \t] Status \t Date
    
    q = (
        pl.scan_csv(
            input_path,
            has_header=False,
            new_columns=["raw_line"],
            separator="\n", # Read full line
            quote_char=None
        )
        .with_columns(
            pl.col("raw_line").str.split("\t").alias("parts")
        )
        .select([
            pl.col("parts").list.get(0).alias("work_key"),
            
            # Logic: If len == 4, index 1 is Edition. If len == 3, Edition is Null.
            pl.when(pl.col("parts").list.len() == 4)
              .then(pl.col("parts").list.get(1))
              .otherwise(pl.lit(None))
              .alias("edition_key"),
              
            # Logic: If len == 4, index 2 is Status. If len == 3, index 1 is Status.
            pl.when(pl.col("parts").list.len() == 4)
              .then(pl.col("parts").list.get(2))
              .otherwise(pl.col("parts").list.get(1))
              .alias("status"),
              
            # Logic: Last column is always Date
            pl.col("parts").list.last().alias("log_date")
        ])
        .with_columns(
             pl.col("log_date").str.to_date(format="%Y-%m-%d", strict=False)
        )
    )
    
    q.sink_parquet(output_path)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    print("Starting ETL pipeline...")
    
    # Process all available dumps
    try:
        process_works()
        process_editions()
        process_authors()
        process_ratings()
        process_reading_log()
        print("\nAll conversions complete! Data available in data/processed/")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
