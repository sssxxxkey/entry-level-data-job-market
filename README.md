# Entry-Level Data Job Market Analytics

A self-directed portfolio project using public U.S. Data Analyst job postings. The goal is to practice Python, SQL, Pandas, and Tableau while answering practical questions about entry-level hiring.

## Project questions

1. Which skills appear most often in entry-level data job postings?
2. How does skill demand differ by role, location, and work arrangement?
3. How often do employers disclose salary?
4. Which skills should a student prioritize?

## Data source

- Kaggle: [Data Analyst Job Postings — Pay, Skills, Benefits](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search)
- Publisher: Luke Barousse
- License listed on Kaggle: Apache 2.0

Download `gsearch_jobs.csv` and place it in `data/raw/`. The raw dataset is excluded from GitHub because it is large.

## Your workflow

### 1. Understand the data
- Load the CSV with Pandas.
- Record its shape, columns, data types, missing values, and duplicate counts.
- Read representative titles and descriptions before defining “entry level.”

### 2. Clean the postings
- Remove duplicate job IDs.
- Standardize dates, locations, salaries, and remote-work indicators.
- Create and justify your own entry-level rule.
- Audit false positives such as senior, manager, lead, and director roles.

### 3. Normalize skills
- Inspect `description_tokens`.
- Convert the stored lists into one row per job-skill pair.
- Standardize aliases such as `power_bi` and `Power BI`.

### 4. Analyze with SQL
- Load clean tables into SQLite.
- Calculate skill frequency with distinct job counts.
- Compare roles, locations, remote work, and disclosed salaries.

### 5. Build a Tableau dashboard
- Market overview
- Top skills
- Role × skill comparison
- Location and remote-work filters
- A learning roadmap supported by your analysis

## Run

```bash
python -m pip install -r requirements.txt
python src/prepare_data.py --input data/raw/gsearch_jobs.csv
```

The starter files intentionally contain `TODO` sections rather than completed analysis. Commit after each meaningful milestone so the repository shows your own process.
