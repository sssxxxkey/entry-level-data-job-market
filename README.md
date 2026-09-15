# Entry-Level Data Job Market Analytics

An end-to-end Python and SQL project that turns public U.S. Data Analyst job postings into an internship-preparation roadmap. The analysis focuses on entry-level and junior roles, compares skill demand across role families and locations, and produces Tableau-ready data.

## Questions answered

1. Which technical skills appear most often in entry-level data job postings?
2. How does skill demand differ across analyst role families?
3. Which U.S. locations have the most entry-level opportunities?
4. How often do postings disclose salary, offer remote work, or request prior experience?
5. What should a student learn first to cover the broadest share of postings?

## Data source

- Kaggle: [Data Analyst Job Postings — Pay, Skills, Benefits](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search)
- Publisher: Luke Barousse
- Coverage in the downloaded snapshot: November 2022–April 2025
- Geography/search scope: United States, `data analyst`
- License shown on Kaggle: Apache 2.0

The raw CSV is intentionally excluded from version control because it is large. Download the Kaggle ZIP and extract `gsearch_jobs.csv` to `data/raw/`, or pass a different input path to the preparation script.

## Project structure

```text
entry-level-data-job-market/
├── data/processed/          # Analysis and Tableau-ready CSV files
├── notebooks/              # Reproducible analysis notebook
├── outputs/                # Charts and summary workbook
├── sql/                    # SQLite schema and analysis queries
├── src/                    # Data preparation and analysis scripts
├── README.md
└── requirements.txt
```

## Reproduce the analysis

```bash
python -m pip install -r requirements.txt
python src/prepare_data.py --input data/raw/gsearch_jobs.csv
python src/run_analysis.py
```

The first script cleans and deduplicates postings, applies the documented entry-level classifier, normalizes skills and locations, and writes a SQLite database. The second script runs the SQL analysis and exports charts and summary tables.

## Entry-level definition

A posting is included when it meets one of these rules:

- its title contains `entry level`, `junior`, `jr`, `graduate`, `new grad`, or `early career`; or
- its description explicitly asks for 0–2 years of experience; or
- its description states that no prior experience is required.

Postings with seniority indicators such as `senior`, `lead`, `manager`, `director`, `principal`, or `staff` in the title are excluded. This is a transparent, rule-based classifier rather than a claim that every employer labels experience consistently.

## Tableau dashboard plan

Use `data/processed/tableau_job_skills.csv` as the primary source and relate it to `jobs_clean.csv` on `job_key`.

- Overview: posting count, salary disclosure rate, remote share, and median advertised annual salary.
- Skills: ranked bars for skill frequency; filters for role family, state, remote status, and posting year.
- Roles and locations: heat map of skill demand by role family and state.
- Roadmap: cumulative posting coverage from learning SQL, Excel, Python, Tableau/Power BI, and cloud tools.

## Limitations

- The source is a rolling Google Jobs search for Data Analyst, not a census of all U.S. openings.
- Job descriptions and salary fields are employer-supplied and may be incomplete.
- Entry-level classification and sector labels are rule-based; the processed data retains the signals so they can be audited.
- Posting dates reflect the source snapshot and should not be presented as current market conditions.

