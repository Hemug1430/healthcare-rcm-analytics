# 🏥 Healthcare Revenue Cycle Management (RCM) & A/R Analytics

![Healthcare RCM Dashboard](dashboard_screenshot.png)

---

## 📌 Executive Summary
Revenue Cycle Management (RCM) in healthcare is heavily impacted by uncollected Accounts Receivable (A/R) and high claim denial rates. This portfolio project delivers a full-stack, end-to-end analytics and machine learning pipeline that simulates, analyzes, predicts, and visualizes healthcare financial data across commercial and government insurance payers (Aetna, BCBS, Cigna, Medicare, UnitedHealthcare).

By leveraging Python, MySQL, Scikit-Learn, and Power BI, this project demonstrates how data engineering and predictive analytics can help healthcare providers reduce A/R aging days, isolate CARC denial drivers, and increase the Net Collection Rate (NCR).

---

## 🛠️ Tech Stack & Systems Architecture
- **Data Engineering & Generation**: Python 3.11 (Pandas, NumPy)
- **Database Warehousing**: MySQL Workbench 8.0 (Relational Schemas, Window Functions, Views)
- **Machine Learning**: Scikit-Learn (Random Forest Classifier, Joblib, Feature Encoding)
- **Business Intelligence**: Power BI Desktop (DAX Modeling, Custom Themes, Interactive Dashboards)
- **Environment & Version Control**: Git, GitHub, VS Code

```text
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 SYSTEM WORKFLOW                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
  [1. Python ETL]          [2. MySQL Staging]        [3. Scikit-Learn ML]      [4. Power BI]
  generate_data.py   ───►  `fact_claims` DB    ───►  train_denial_model.py ──► Interactive
  (1,000 Claims)           (SQL Aging Buckets)       (Random Forest Model)     Dashboard




  💡 Key Business KPIs & Metrics
Total Billed Amount: $2.57M (Total initial claim revenue billed)

Total Outstanding A/R: $1.12M (Uncollected revenue across aging buckets)

Net Collection Rate (NCR): 56.39% (Percentage of allowed amounts actually collected)

Initial Denial Rate: 15.50% (Proportion of claims rejected on first submission)

Total Collections Captured: $1.45M (Actual revenue received from payers)

📁 Repository Structure

healthcare-rcm-analytics/
├── .gitignore                      # Git exclusion file
├── README.md                       # Repository documentation
├── requirements.txt                # Python package dependencies
├── dashboard_screenshot.png        # Power BI executive dashboard view
├── data/
│   └── synthetic_rcm_claims.csv    # Raw synthetic dataset (1,000 records)
├── scripts/
│   ├── generate_data.py            # Data generation pipeline script
│   └── train_denial_model.py       # Random Forest ML model training script
├── Sql/
│   ├── schema.sql                  # MySQL database and table schema
│   └── analytics_queries.sql       # SQL scripts (Aging buckets, DENSE_RANK)
└── Insights/
    ├── Healthcare_RCM_Dashboard.pbix # Power BI report file
    └── model_metrics.json          # Machine Learning evaluation metrics


    🔬 Project Modules & Implementation Details
1. Data Pipeline & Engineering (scripts/generate_data.py)
Programmatically generated 1,000 realistic claims records containing attributes such as Claim_ID, Patient_ID, Payer, Billed_Amount, Paid_Amount, Claim_Date, Status (Paid, Denied, Outstanding), and Denial_Reason.

Exported clean CSV data to data/synthetic_rcm_claims.csv.


2. Relational Database & SQL Analytics (Sql/)Staged claims data inside a structured MySQL table (fact_claims).
A/R Aging Analysis: Formatted uncollected balances into 30-day aging buckets ($0–30$, $31–60$, $61–90$, $90+$ days) to isolate high-risk revenue balances per payer.
Payer Denial Drivers: Executed DENSE_RANK() SQL window functions to group and rank primary Claim Adjustment Reason Codes 
(CARCs):CO-27: Coverage terminated prior to service
 dateCO-18: Duplicate claim 
 serviceCO-16: Claim/service lacks necessary details 
formattingCO-50: Non-covered service or policy exclusion


# 3. Machine Learning Predictive Pipeline (scripts/train_denial_model.py)Feature-engineered input attributes (Payer, Billed_Amount, Procedure_Category) to predict whether a claim will be Denied or Paid.
Trained a Random Forest Classifier with Scikit-learn, utilizing label encoding and train-test splits ($80/20$).
Evaluation output saved to Insights/ to support proactive claim auditing before clearinghouse submission.

4. Power BI Executive Dashboard (Insights/Healthcare_RCM_Dashboard.pbix)
Interactive UI: Built a clean 3-column layout featuring high-contrast KPI cards, a slicer pane, and rounded-corner visual containers.

Key Visualizations:

Stacked Bar Chart: Outstanding A/R by 30-day aging bins categorized by Payer.

Horizontal Bar Chart: Frequency distribution of top CARC denial codes (CO-16 through CO-50).

Donut Chart: Paid revenue distribution by Payer ($1.45M total).

DAX Measures: Implemented explicit DAX logic for Net Collection Rate, Denial Rate, Total Billed, and Total Outstanding AR.