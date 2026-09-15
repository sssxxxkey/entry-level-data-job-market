"""Run SQL summaries and export portfolio charts."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data/job_market.db"
PROCESSED = ROOT / "data/processed"
CHARTS = ROOT / "outputs/charts"


def query(conn, sql):
    return pd.read_sql_query(sql, conn)


def bar_svg(frame: pd.DataFrame, label: str, value: str, title: str, path: Path, color: str) -> None:
    rows = frame.sort_values(value, ascending=False).head(15).reset_index(drop=True)
    width, left, right, top, row_h = 900, 190, 50, 70, 30
    height = top + len(rows) * row_h + 55
    max_value = max(float(rows[value].max()), 1)
    items = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="24" y="36" font-family="Arial" font-size="20" font-weight="bold" fill="#17324D">{title}</text>']
    for i, row in rows.iterrows():
        y = top + i * row_h
        bar_w = (width-left-right) * float(row[value]) / max_value
        items += [f'<text x="{left-10}" y="{y+17}" text-anchor="end" font-family="Arial" font-size="13" fill="#25364A">{row[label]}</text>',
                  f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="20" rx="2" fill="{color}"/>',
                  f'<text x="{left+bar_w+7:.1f}" y="{y+16}" font-family="Arial" font-size="12" fill="#25364A">{int(row[value]):,}</text>']
    items.append('</svg>')
    path.write_text('\n'.join(items), encoding='utf-8')


def main() -> None:
    CHARTS.mkdir(parents=True, exist_ok=True)
    navy, blue = "#17324D", "#2C7FB8"
    with sqlite3.connect(DB) as conn:
        overview = query(conn, """SELECT COUNT(*) postings,
          ROUND(100.0*AVG(salary_disclosed),1) salary_disclosure_pct,
          ROUND(100.0*AVG(remote_status='Remote allowed'),1) remote_pct,
          ROUND(AVG(CASE WHEN salary_disclosed THEN salary_annual END),0) avg_disclosed_salary
          FROM jobs""")
        skills = query(conn, """SELECT skill, COUNT(DISTINCT job_key) postings,
          ROUND(100.0*COUNT(DISTINCT job_key)/(SELECT COUNT(*) FROM jobs),1) posting_coverage_pct
          FROM job_skills GROUP BY skill ORDER BY postings DESC LIMIT 15""")
        roles = query(conn, """SELECT role_family, COUNT(*) postings FROM jobs
          GROUP BY role_family ORDER BY postings DESC""")
        states = query(conn, """SELECT state, COUNT(*) postings FROM jobs
          WHERE state <> 'Remote/Unspecified' GROUP BY state ORDER BY postings DESC LIMIT 15""")
        heat = query(conn, """SELECT role_family, skill, COUNT(DISTINCT job_key) postings
          FROM job_skills WHERE skill IN ('SQL','Excel','Python','Tableau','Power BI','R')
          GROUP BY role_family, skill""")
        years = query(conn, """SELECT posting_year, COUNT(*) postings FROM jobs
          GROUP BY posting_year ORDER BY posting_year""")

    overview.to_csv(PROCESSED / "summary_overview.csv", index=False)
    skills.to_csv(PROCESSED / "summary_skills.csv", index=False)
    roles.to_csv(PROCESSED / "summary_roles.csv", index=False)
    states.to_csv(PROCESSED / "summary_states.csv", index=False)
    years.to_csv(PROCESSED / "summary_years.csv", index=False)

    bar_svg(skills, "skill", "postings", "Skills requested in entry-level data analyst postings", CHARTS / "top_skills.svg", blue)
    bar_svg(roles, "role_family", "postings", "Entry-level postings by role family", CHARTS / "role_families.svg", navy)
    print(overview.to_string(index=False))
    print(skills.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
