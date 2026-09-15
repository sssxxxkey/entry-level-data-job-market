"""Starter analysis script. Add your own queries and charts after cleaning."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data/job_market.db"


def main() -> None:
    # TODO 1: connect to your SQLite database.
    # TODO 2: answer each question in sql/analysis.sql.
    # TODO 3: validate the SQL results against Pandas.
    # TODO 4: export clearly labelled charts and summary tables.
    raise NotImplementedError("TODO: build your analysis")


if __name__ == "__main__":
    main()
