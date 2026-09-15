"""Clean Kaggle job postings and build analysis-ready CSV and SQLite files."""

from __future__ import annotations

import argparse
import ast
import re
import sqlite3
from pathlib import Path

import pandas as pd


SKILL_ALIASES = {
    "sql": "SQL", "python": "Python", "r": "R", "excel": "Excel",
    "tableau": "Tableau", "power bi": "Power BI", "power_bi": "Power BI",
    "looker": "Looker", "snowflake": "Snowflake", "aws": "AWS",
    "azure": "Azure", "gcp": "GCP", "spark": "Spark", "hadoop": "Hadoop",
    "sas": "SAS", "sap": "SAP", "oracle": "Oracle", "mysql": "MySQL",
    "postgresql": "PostgreSQL", "powerpoint": "PowerPoint", "word": "Word",
    "airflow": "Airflow", "databricks": "Databricks", "git": "Git",
    "javascript": "JavaScript", "java": "Java", "c++": "C++", "go": "Go",
    "qlik": "Qlik", "alteryx": "Alteryx", "scikit-learn": "scikit-learn",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "numpy": "NumPy",
    "pandas": "Pandas", "matplotlib": "Matplotlib", "seaborn": "Seaborn",
}

STATE_RE = re.compile(r",\s*([A-Z]{2})(?:\s|$)")
EXPLICIT_ENTRY = re.compile(
    r"\b(?:entry[- ]?level|junior|jr\.?|new grad(?:uate)?|graduate program|early career|recent graduate)\b",
    re.I,
)
ZERO_TO_TWO = re.compile(
    r"\b(?:0|zero|one|1|two|2)\s*(?:-|to|–)\s*(?:1|one|2|two)\+?\s*years?\b|"
    r"\b(?:0|1|one|2|two)\+?\s*years?\s+(?:of\s+)?(?:relevant\s+)?experience\b|"
    r"\bno (?:prior|previous|professional) experience (?:is )?required\b",
    re.I,
)
SENIOR_TITLE = re.compile(r"\b(?:senior|sr\.?|lead|manager|director|principal|staff|head|vp|vice president)\b", re.I)


def role_family(title: str) -> str:
    t = title.lower()
    if "business intelligence" in t or re.search(r"\bbi\b", t): return "Business Intelligence"
    if "financial" in t or "finance" in t: return "Financial Analyst"
    if "marketing" in t: return "Marketing Analyst"
    if "business" in t: return "Business Analyst"
    if "operations" in t or "operational" in t: return "Operations Analyst"
    if "health" in t or "clinical" in t: return "Healthcare Analyst"
    if "risk" in t or "fraud" in t: return "Risk/Fraud Analyst"
    if "data scientist" in t or "data science" in t: return "Data Science"
    if "data engineer" in t: return "Data Engineering"
    return "Data Analyst"


def sector_signal(text: str) -> str:
    patterns = [
        ("Healthcare", r"\b(healthcare|hospital|clinical|patient|medical)\b"),
        ("Finance", r"\b(bank|banking|financial services|insurance|fintech|credit union)\b"),
        ("Technology", r"\b(software|technology|saas|cloud platform|information technology)\b"),
        ("Retail", r"\b(retail|e-commerce|ecommerce|consumer goods)\b"),
        ("Government/Education", r"\b(government|public sector|university|college|school district)\b"),
        ("Consulting", r"\b(consulting|consultancy|professional services)\b"),
        ("Manufacturing", r"\b(manufacturing|factory|industrial|automotive)\b"),
    ]
    for label, pattern in patterns:
        if re.search(pattern, text, re.I): return label
    return "Other/Unclear"


def parse_skills(value: object) -> list[str]:
    if pd.isna(value): return []
    try:
        raw = ast.literal_eval(str(value))
    except (ValueError, SyntaxError):
        raw = []
    found = []
    for item in raw if isinstance(raw, list) else []:
        key = str(item).strip().lower()
        found.append(SKILL_ALIASES.get(key, str(item).strip().title()))
    return sorted(set(x for x in found if x))


def prepare(input_path: Path, output_dir: Path, db_path: Path) -> None:
    usecols = ["title", "company_name", "location", "via", "description", "job_id",
               "schedule_type", "work_from_home", "salary_avg", "salary_yearly",
               "date_time", "description_tokens"]
    df = pd.read_csv(input_path, usecols=usecols, low_memory=False)
    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce")
    df = df.sort_values("date_time").drop_duplicates("job_id", keep="last").copy()
    df["title"] = df["title"].fillna("").str.strip()
    df["description"] = df["description"].fillna("")
    df["location"] = df["location"].fillna("").str.replace(r"\s+", " ", regex=True).str.strip()

    combined = df["title"] + " " + df["description"]
    df["entry_signal"] = combined.str.extract(f"({EXPLICIT_ENTRY.pattern})", flags=re.I, expand=False).fillna("")
    exp_signal = combined.str.extract(f"({ZERO_TO_TWO.pattern})", flags=re.I, expand=False).fillna("")
    df.loc[df["entry_signal"].eq(""), "entry_signal"] = exp_signal
    mask = df["entry_signal"].ne("") & ~df["title"].str.contains(SENIOR_TITLE, na=False)
    jobs = df.loc[mask].copy()

    jobs["job_key"] = range(1, len(jobs) + 1)
    jobs["posting_date"] = jobs["date_time"].dt.date.astype("string")
    jobs["posting_year"] = jobs["date_time"].dt.year.astype("Int64")
    jobs["role_family"] = jobs["title"].map(role_family)
    jobs["sector_signal"] = (jobs["company_name"].fillna("") + " " + jobs["description"]).map(sector_signal)
    jobs["state"] = jobs["location"].str.extract(STATE_RE, expand=False).fillna("Remote/Unspecified")
    remote_text = jobs["work_from_home"].fillna(False).astype(str).str.lower().eq("true") | jobs["location"].str.contains("anywhere|remote", case=False, na=False)
    jobs["remote_status"] = remote_text.map({True: "Remote allowed", False: "On-site/Unspecified"})
    jobs["salary_annual"] = pd.to_numeric(jobs["salary_yearly"], errors="coerce")
    jobs["salary_disclosed"] = jobs["salary_annual"].notna()
    jobs["schedule_type"] = jobs["schedule_type"].fillna("Unspecified")
    jobs["source_platform"] = jobs["via"].fillna("Unknown").str.replace(r"^via\s+", "", regex=True)
    jobs["skills"] = jobs["description_tokens"].map(parse_skills)
    jobs["skill_count"] = jobs["skills"].str.len()

    keep = ["job_key", "job_id", "title", "company_name", "location", "state", "role_family",
            "sector_signal", "posting_date", "posting_year", "schedule_type", "remote_status",
            "salary_disclosed", "salary_annual", "source_platform", "entry_signal", "skill_count"]
    clean = jobs[keep].copy()
    skills = jobs[["job_key", "job_id", "role_family", "state", "sector_signal", "posting_year",
                   "remote_status", "salary_annual", "skills"]].explode("skills").rename(columns={"skills": "skill"})
    skills = skills.dropna(subset=["skill"])
    skills["skill_group"] = skills["skill"].map(lambda x: "Core analytics" if x in {"SQL", "Python", "R", "Excel"} else
                                                "Visualization" if x in {"Tableau", "Power BI", "Looker", "Qlik"} else
                                                "Cloud/data platform" if x in {"AWS", "Azure", "GCP", "Snowflake", "Spark", "Databricks", "Hadoop"} else
                                                "Other")

    output_dir.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_dir / "jobs_clean.csv", index=False)
    skills.to_csv(output_dir / "tableau_job_skills.csv", index=False)

    with sqlite3.connect(db_path) as conn:
        clean.to_sql("jobs", conn, if_exists="replace", index=False)
        skills.to_sql("job_skills", conn, if_exists="replace", index=False)
        conn.executescript("""
            CREATE INDEX IF NOT EXISTS idx_jobs_role ON jobs(role_family);
            CREATE INDEX IF NOT EXISTS idx_jobs_state ON jobs(state);
            CREATE INDEX IF NOT EXISTS idx_skills_skill ON job_skills(skill);
            CREATE INDEX IF NOT EXISTS idx_skills_job ON job_skills(job_key);
        """)
    print(f"Prepared {len(clean):,} entry-level postings and {len(skills):,} job-skill rows.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--database", type=Path, default=Path("data/job_market.db"))
    args = parser.parse_args()
    prepare(args.input, args.output_dir, args.database)
