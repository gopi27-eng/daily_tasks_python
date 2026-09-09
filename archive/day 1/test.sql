WITH RankedSwipes AS (
    SELECT 
        contractor_id,
        zone,
        access_time,
        ROW_NUMBER() OVER (PARTITION BY contract_id ORDER BY access_time) AS swipe_rank
    FROM cargo_access_logs
)
SELECT * 
FROM RankedSwipe 
WHERE swipe_rank  = 1;