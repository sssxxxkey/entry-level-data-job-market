# Tableau dashboard guide

## Connect the data

1. Add `data/processed/jobs_clean.csv`.
2. Add `data/processed/tableau_job_skills.csv`.
3. Create a relationship from `jobs_clean.job_key` to `tableau_job_skills.job_key`.
4. Use `COUNTD(job_key)` for posting counts to avoid double-counting jobs with several skills.

## Suggested sheets

### Market overview

- Total postings: `COUNTD(job_key)`
- Remote share: percent of postings where `remote_status = 'Remote allowed'`
- Salary disclosure: percent where `salary_disclosed = True`
- Average disclosed salary: average `salary_annual`, excluding nulls

### Skill demand

- Rows: `skill`
- Columns: `COUNTD(job_key)`
- Filter: top 15 by posting count
- Tooltip: posting count and percent of all selected postings

### Role × skill heat map

- Rows: `role_family`
- Columns: `skill`
- Color/label: `COUNTD(job_key)`
- Filter skills to SQL, Excel, Python, Tableau, Power BI, and R

### Location view

- Detail: `state`
- Color: `COUNTD(job_key)`
- Filters: role family, skill, remote status, posting year

## Dashboard layout

Use a 1,200 × 800 fixed canvas. Put four KPI tiles across the top, skill demand on the left, the role-skill heat map on the right, and filters in a narrow side panel. Include the snapshot dates and the location-sampling caveat in the footer.

