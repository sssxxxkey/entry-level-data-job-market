"""Starter pipeline. Complete each TODO yourself."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd


def load_data(path: Path) -> pd.DataFrame:
    # TODO 1: read the CSV and inspect its shape and columns.
    raise NotImplementedError("TODO: implement load_data")


def clean_postings(df: pd.DataFrame) -> pd.DataFrame:
    # TODO 2: remove duplicate job IDs.
    # TODO 3: parse dates and standardize missing values.
    # TODO 4: normalize remote and annual salary fields.
    raise NotImplementedError("TODO: implement clean_postings")


def classify_entry_level(df: pd.DataFrame) -> pd.DataFrame:
    # TODO 5: define inclusion signals from titles/descriptions.
    # TODO 6: exclude senior roles and audit sample matches.
    raise NotImplementedError("TODO: implement classify_entry_level")


def build_skill_table(jobs: pd.DataFrame) -> pd.DataFrame:
    # TODO 7: safely parse description_tokens.
    # TODO 8: explode skills and standardize aliases.
    raise NotImplementedError("TODO: implement build_skill_table")


def validate(jobs: pd.DataFrame, skills: pd.DataFrame) -> None:
    # TODO 9: add at least three meaningful assertions.
    raise NotImplementedError("TODO: implement validation checks")


def main(input_path: Path) -> None:
    raw = load_data(input_path)
    clean = clean_postings(raw)
    jobs = classify_entry_level(clean)
    skills = build_skill_table(jobs)
    validate(jobs, skills)
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    # TODO 10: save your clean CSV and SQLite tables.


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    main(args.input)
