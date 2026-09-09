SELECT 
   pilot_id, 
   flight_date,
   flight_hours
FROM (
    SELECT
       pilot_id,
       flight_date,
       flight_hours,
       ROW_NUMBER() OVER(
        PARTITION BY pilot_id 
       ORDER BY flight_date DESC) AS rn
       FROM pilot_logbook
       ) AS row_number
WHERE rn = 1;