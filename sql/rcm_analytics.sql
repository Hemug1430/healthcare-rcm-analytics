USE healthcare;

-- Query 1: A/R Aging Buckets
SELECT 
    payer,
    COUNT(claim_id) AS total_claims,
    SUM(outstanding_balance) AS total_outstanding_ar,
    SUM(CASE WHEN aging_days BETWEEN 0 AND 30 THEN outstanding_balance ELSE 0 END) AS aging_0_30,
    SUM(CASE WHEN aging_days BETWEEN 31 AND 60 THEN outstanding_balance ELSE 0 END) AS aging_31_60,
    SUM(CASE WHEN aging_days BETWEEN 61 AND 90 THEN outstanding_balance ELSE 0 END) AS aging_61_90,
    SUM(CASE WHEN aging_days > 90 THEN outstanding_balance ELSE 0 END) AS aging_90_plus
FROM healthcare_dataset
WHERE status != 'Paid'
GROUP BY payer
ORDER BY total_outstanding_ar DESC;

-- Query 2: Top Denial Driver per Payer
WITH PayerDenials AS (
    SELECT 
        payer,
        denial_reason,
        COUNT(claim_id) AS denial_count,
        DENSE_RANK() OVER (PARTITION BY payer ORDER BY COUNT(claim_id) DESC) as rnk
    FROM healthcare_dataset
    WHERE status = 'Denied'
    GROUP BY payer, denial_reason
)
SELECT payer, denial_reason, denial_count
FROM PayerDenials
WHERE rnk = 1;