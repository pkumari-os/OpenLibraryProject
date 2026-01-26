
import polars as pl

# Schema for Edition Dump
# Strictly limited to fields used in process_data.py
EDITION_SCHEMA = pl.Struct({
    "publish_date": pl.Utf8,
    "works": pl.List(pl.Struct({
        "key": pl.Utf8
    }))
})
