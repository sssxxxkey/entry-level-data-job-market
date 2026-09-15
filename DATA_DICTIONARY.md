# Data dictionary

## `jobs_clean.csv`

| Column | Description |
|---|---|
| `job_key` | Sequential project key used to relate tables |
| `job_id` | Source job identifier |
| `title` | Cleaned posting title |
| `company_name` | Employer name from the source |
| `location` | Original cleaned location text |
| `state` | Two-letter U.S. state extracted from location, or `Remote/Unspecified` |
| `role_family` | Rule-based title group |
| `sector_signal` | Heuristic sector inferred from employer and description keywords |
| `posting_date`, `posting_year` | Source snapshot timestamp |
| `schedule_type` | Full-time, part-time, contract, or unspecified |
| `remote_status` | `Remote allowed` or `On-site/Unspecified` |
| `salary_disclosed` | Whether an annual salary value is available |
| `salary_annual` | Source-standardized annual salary when available |
| `source_platform` | Platform named in the Google Jobs result |
| `entry_signal` | Text matched by the entry-level classifier |
| `skill_count` | Number of normalized skills attached to the posting |

## `tableau_job_skills.csv`

One row per posting-skill pair. Join or relate to `jobs_clean.csv` using `job_key`. `skill_group` organizes skills into core analytics, visualization, cloud/data platform, and other categories.

## Summary files

`summary_overview.csv`, `summary_skills.csv`, `summary_roles.csv`, `summary_states.csv`, and `summary_years.csv` contain the exact aggregates used in the workbook and charts.

