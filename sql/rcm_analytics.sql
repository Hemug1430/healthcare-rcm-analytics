-- 1. Create Fact Table in healthcare database
USE healthcare;

DROP TABLE IF EXISTS fact_claims;

CREATE TABLE fact_claims (
    claim_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20),
    payer VARCHAR(50),
    billed_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    outstanding_balance DECIMAL(10,2),
    status VARCHAR(20),
    denial_reason VARCHAR(100),
    claim_date DATE,
    aging_days INT
);

-- 2. Analytical Query: A/R Aging Buckets (0-30, 31-60, 61-90, 90+ days)
SELECT 
    payer,
    COUNT(claim_id) AS total_claims,
    SUM(outstanding_balance) AS total_outstanding_ar,
    SUM(CASE WHEN aging_days BETWEEN 0 AND 30 THEN outstanding_balance ELSE 0 END) AS aging_0_30,
    SUM(CASE WHEN aging_days BETWEEN 31 AND 60 THEN outstanding_balance ELSE 0 END) AS aging_31_60,
    SUM(CASE WHEN aging_days BETWEEN 61 AND 90 THEN outstanding_balance ELSE 0 END) AS aging_61_90,
    SUM(CASE WHEN aging_days > 90 THEN outstanding_balance ELSE 0 END) AS aging_90_plus
FROM fact_claims
WHERE status != 'Paid'
GROUP BY payer
ORDER BY total_outstanding_ar DESC;

-- 3. Analytical Query: Top Denial Reasons by Payer using Window Function
WITH PayerDenials AS (
    SELECT 
        payer,
        denial_reason,
        COUNT(claim_id) AS denial_count,
        DENSE_RANK() OVER (PARTITION BY payer ORDER BY COUNT(claim_id) DESC) as rnk
    FROM fact_claims
    WHERE status = 'Denied'
    GROUP BY payer, denial_reason
)
SELECT payer, denial_reason, denial_count
FROM PayerDenials
WHERE rnk = 1;