
import polars as pl

# Schema for Work Dump
# Strictly limited to fields used in process_data.py to avoid polymorphic errors
WORK_SCHEMA = pl.Struct({
    "title": pl.Utf8,
    "subjects": pl.List(pl.Utf8),
})
