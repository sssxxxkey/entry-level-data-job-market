-- Portfolio queries for the entry-level data job market dashboard.

-- 1. Overall market snapshot
SELECT COUNT(*) AS postings,
       ROUND(100.0 * AVG(salary_disclosed), 1) AS salary_disclosure_pct,
       ROUND(100.0 * AVG(remote_status = 'Remote allowed'), 1) AS remote_pct,
       ROUND(AVG(salary_annual), 0) AS avg_disclosed_salary
FROM jobs;

-- 2. Most requested skills and posting coverage
SELECT skill,
       COUNT(DISTINCT job_key) AS postings,
       ROUND(100.0 * COUNT(DISTINCT job_key) / (SELECT COUNT(*) FROM jobs), 1) AS posting_coverage_pct
FROM job_skills
GROUP BY skill
ORDER BY postings DESC
LIMIT 20;

-- 3. Skill demand by analyst role family
SELECT role_family, skill, COUNT(DISTINCT job_key) AS postings
FROM job_skills
WHERE skill IN ('SQL', 'Excel', 'Python', 'Tableau', 'Power BI', 'R')
GROUP BY role_family, skill
ORDER BY role_family, postings DESC;

-- 4. Leading U.S. locations
SELECT state, COUNT(*) AS postings,
       ROUND(100.0 * AVG(remote_status = 'Remote allowed'), 1) AS remote_pct
FROM jobs
GROUP BY state
HAVING state <> 'Remote/Unspecified'
ORDER BY postings DESC
LIMIT 15;

-- 5. Salary disclosure by role family (disclosed annual salaries only)
SELECT role_family, COUNT(*) AS postings,
       SUM(salary_disclosed) AS disclosed_salaries,
       ROUND(AVG(CASE WHEN salary_disclosed THEN salary_annual END), 0) AS avg_salary
FROM jobs
GROUP BY role_family
HAVING SUM(salary_disclosed) >= 5
ORDER BY avg_salary DESC;

