
import polars as pl

# Schema for Author Dump
# Strictly limited to fields used in process_data.py
AUTHOR_SCHEMA = pl.Struct({
    "name": pl.Utf8,
    "birth_date": pl.Utf8,
})
