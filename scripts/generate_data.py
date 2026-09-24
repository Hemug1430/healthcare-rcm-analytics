import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# 1. Set parameters for data generation
num_claims = 1000  # Number of rows to generate
payers = ["Aetna", "BCBS", "Medicare", "UnitedHealthcare", "Cigna"]
statuses = ["Paid", "Denied", "Pending"]
denial_reasons = {
    "CO-18": "Duplicate claim",
    "CO-27": "Expenses incurred after coverage terminated",
    "CO-16": "Claim lacks information",
    "CO-50": "Non-covered services",
}

# 2. Initialize lists to hold our data
data = []
start_date = datetime(2025, 1, 1)

for i in range(1, num_claims + 1):
    # Claim & Patient Info
    claim_id = f"CLM-{100000 + i}"
    patient_id = f"PT-{200000 + random.randint(1, 300)}"  # Some patients have multiple claims
    payer = random.choice(payers)

    # Date & Aging
    days_offset = random.randint(0, 365)
    claim_date = start_date + timedelta(days=days_offset)
    aging_days = random.randint(1, 120)

    # Financials
    billed_amount = round(random.uniform(150.0, 5000.0), 2)

    # RCM Metrics Logic
    status = random.choices(statuses, weights=[0.70, 0.15, 0.15], k=1)[0]  # 70% Paid, 15% Denied, 15% Pending

    if status == "Paid":
        paid_amount = round(billed_amount * random.uniform(0.6, 1.0), 2)
        outstanding_balance = round(billed_amount - paid_amount, 2)
        denial_reason = np.nan
    elif status == "Denied":
        paid_amount = 0.0
        outstanding_balance = billed_amount
        denial_reason = random.choice(list(denial_reasons.keys()))
    else:  # Pending
        paid_amount = 0.0
        outstanding_balance = billed_amount
        denial_reason = np.nan

    data.append(
        {
            "Claim_ID": claim_id,
            "Patient_ID": patient_id,
            "Payer": payer,
            "Claim_Date": claim_date.strftime("%Y-%m-%d"),
            "Billed_Amount": billed_amount,
            "Paid_Amount": paid_amount,
            "Outstanding_Balance": outstanding_balance,
            "Status": status,
            "Denial_Reason": denial_reason,
            "Aging_Days": aging_days,
        }
    )

# 3. Create DataFrame and export to CSV
df = pd.DataFrame(data)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

output_path = "data/synthetic_rcm_claims.csv"
df.to_csv(output_path, index=False)
print(f"\n Success! Generated {num_claims} claims and saved to '{output_path}'")