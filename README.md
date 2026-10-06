Care Transition Efficiency & Placement Outcome Analytics

Project Overview

This project analyzes the operational flow of children through the Unaccompanied Alien Children (UAC) care pipeline:

CBP Intake / Custody → Transfer to HHS Care → Discharge / Sponsor Placement

The project measures transition efficiency, discharge performance, stage pressure, bottlenecks, stagnation periods, and outcome trends over time.

Business Problem

The project addresses four main questions:

How efficiently are children transferred from CBP custody to HHS care?

Are HHS discharges keeping pace with observed pipeline activity?

Where and when does stage pressure accumulate?

Are transition and discharge outcomes improving or deteriorating over time?

Objectives

Measure CBP → HHS transition efficiency.

Evaluate HHS discharge effectiveness.

Identify stage-specific pressure and bottleneck periods.

Analyze outcome trends over time.

Support operational monitoring and process improvement.

Dataset

Core fields include:

Date

CBP Intake

CBP Custody

CBP Transfers

HHS Care

HHS Discharges

Data coverage in the final analytical dataset:

720 reporting observations

January 12, 2023 to December 21, 2025

0 missing values after cleaning

0 duplicate rows after cleaning

The reporting dates are not continuous calendar coverage, so the dataset represents reporting observations rather than a complete daily time series.

Analytical Workflow

Data understanding and quality checks

Data cleaning and transformation

Exploratory data analysis

Monthly, quarterly and yearly analysis

KPI development

Stage-pressure and bottleneck analysis

Stagnation and anomaly detection

Interactive Streamlit dashboard

Key Metrics

Transfer Efficiency Ratio

Discharge Effectiveness Index

Transfer Activity Ratio

Placement Activity Ratio

Exit-to-Entry Activity Ratio

CBP Accumulation Rate

HHS Accumulation Rate

Outcome Stability Score

Total Stage Pressure

Metric Interpretation

The project contains both movement measures and stage stock measures.

CBP Custody and HHS Care are reported stage-stock measures.

Intake, Transfers and Discharges are observed movement measures.

Activity ratios are therefore used as operational comparisons, not as individual-level placement success rates. Stage accumulation measures are treated as pressure proxies because the reporting dates are not complete calendar-day coverage.

Streamlit Dashboard

The dashboard contains four core modules.

1. Care Pipeline Flow Visualization

Shows:

CBP Intake

CBP Custody

CBP Transfers

HHS Care

HHS Discharges

Pipeline activity

Average stage levels

2. Transfer & Discharge Efficiency Panels

Includes:

Transfer Efficiency

Discharge Effectiveness

Transfer Activity Ratio

Placement Activity Ratio

Monthly efficiency trends

Transfer vs discharge activity

3. Bottleneck Detection Charts

Includes:

CBP accumulation pressure

HHS accumulation pressure

Total stage pressure

Threshold-based visual alerts

High-pressure periods

Bottleneck flags

Stagnation flags

Operational anomaly indicators

4. Outcome Trend Analysis

Includes:

Monthly discharge effectiveness

Outcome Stability Score

Average HHS Care

Total HHS Discharges

Year-over-year comparisons

Efficiency trend comparisons

Dashboard Capabilities

Date range selection

Percentage / ratio metric toggle

Adjustable alert thresholds

Dynamic KPI updates

Interactive Plotly charts

Filtered analytical data view

Key Findings

The analysis indicates a major change in operating conditions across the study period.

2023–2024

Pipeline activity volumes were substantially higher.

CBP custody and HHS care levels were materially higher than in 2025.

High-load CBP bottleneck periods were identified.

February 2024 contained unusually high operational observations.

2025

Despite much lower observed activity:

Transfer efficiency deteriorated during the year.

Monthly transfer efficiency declined from approximately 89% in January 2025 to approximately 23% in December 2025.

Discharge effectiveness remained very low for many reporting observations.

Prolonged transfer and discharge stagnation periods were detected.

Lower observed volume did not automatically translate into stronger process performance.

Business Recommendations

Monitor transition efficiency independently from workload volume.

Track CBP and HHS stage pressure separately.

Review repeated stagnation periods at the operational level.

Strengthen monitoring of the discharge stage.

Use configurable thresholds to identify periods requiring attention.

Limitations

Reporting dates are not continuous across the full calendar period.

The dataset does not contain individual child-level case histories.

Different measures may refer to different cohorts or timing windows.

Activity ratios should not be interpreted as individual-level placement probabilities.

Stage accumulation measures are analytical pressure proxies rather than exact backlog counts.

Correlation shows association, not causation.

Project Structure

Care Transition Efficiency & Placement Outcome Analytics/
│
├── app.py
├── final_analytical_dataset.csv
├── requirements.txt
├── README.md
├── .gitignore
├── Care Transition Efficiency & Placement Outcome Analytics.ipynb
├── uac_final_analysis_dataset.csv
├── uac_kpi_summary.csv
├── uac_monthly_analysis.csv
├── uac_quarterly_analysis.csv
├── uac_yearly_analysis.csv
└── data/

Technologies

Python

Pandas

NumPy

Plotly

Streamlit

Jupyter Notebook

Git

GitHub

Run Locally

Install dependencies:

pip install -r requirements.txt

Start the dashboard:

streamlit run app.py

Deployment

The intended deployment workflow is:

Jupyter Notebook
      ↓
Final Analytical Dataset
      ↓
Streamlit App
      ↓
GitHub Repository
      ↓
Streamlit Community Cloud
      ↓
Shareable Dashboard

Source

Project context and source data are based on the project brief referencing Unified Mentor and the U.S. Department of Health and Human Services (HHS).

Author

Care Transition Efficiency & Placement Outcome Analytics
