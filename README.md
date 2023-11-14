# Supercell Data Internship Test - Clash Royale

## Project Overview

This project involves the analysis of a dataset from Supercell's hypothetical free-to-play mobile game, Clash Royale. The dataset includes three tables: `account`, `account_date_session`, and `iap_purchase`. The primary objective is to derive actionable insights related to daily active users (DAU), sales, and geographic revenue distribution.

## Instructions

1. **Getting Started:**
    - Download the SQLite database from [https://supr.cl/testy-test](https://supr.cl/testy-test) with the provided password.
    - Access the database using SQLite3 command line interface or libraries for R and Python.

2. **Code Overview:**
    - The provided code connects to the SQLite database, extracts table descriptions, and performs various analyses using SQL, pandas, matplotlib, geopandas, and pycountry.

3. **Analysis and Visualizations:**

    ### Question 1: Description of Datasets
    - The code retrieves and displays the structure and content of the `account`, `account_date_session`, and `iap_purchase` tables.

    ### Question 2: Analyzing Daily Active Users
    - Plots the changes in DAU over time by both session count and duration.
    - Introduces a new question to visualize the cumulative sum of created accounts over time.

    ### Question 3: Analyzing Sales
    - Analyzes the geographic split of revenue and users.
    - Calculates average revenue per user per market and presents observations.
    - Produces visualizations, including bar charts and a choropleth map illustrating Average Revenue Per User (ARPU) by country.

4. **Conclusion:**
    - Summarizes key findings and insights derived from the analysis.

5. **Submission:**
    - The report and code are expected to be submitted as a PDF through the job application form.

## Notes
- Ensure that the code is reproducible and well-commented.
- Include any additional details, code snippets, or visualizations that support your findings.
- Evaluation will be based on the clarity, insightfulness, and actionability of the report.
