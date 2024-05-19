# shift-schedule-analysis
Data Analysis - Contact center agents shift schedule data

## Files included

1. `Agent Shifts - Sample.txt` -   Raw dataset
2. `convert-data.py`   -   Python script to convert raw dataset to structured csv file
3. `Agent_Shifts_Structured.csv` - Structured csv file after conversion
4. `shift-data-eda.ipynb` - Data preprocessing, EDA, visualizations and answers to business questions
5. `person_activity_durations_report.csv`   -   Report
6. `person_activity_durations_per_date_report`  -   Report
7. `business-questions.md` - Business questions and answers
8. `README.md` - README file

## Steps

0. Clone this repo

1. Convert raw unstructured data from `Agent Shifts - Sample.txt` file to a bit structured format. This should create `Agent_Shifts_Structured.csv` file.
    ```
    python convert-data.py
    ```

2. Run Jupyter notebook `shift-data-eda.ipynb`. This should generare 2 report files in csv format.

## Next steps

This data analysis was a quick first attempt to get answers to business questions. Here are possible next steps for further iterations:

- Collect information about data update frequency - Daily/Weekly/Monthly, Incremental? etc.
- High-level data system design
- ETL/ELT data pipeline - Workflow orchestrator/DAGs, Data lake, OLAP Data Warehouse
- Data modeling - star schema with dimension and fact tables
- Dashboard/visualizations
- Data analysis report
- Optimizations
    - Data extraction - explore NLP/LLM to improve data extraction from raw input files
    - Find ways to make data more structured