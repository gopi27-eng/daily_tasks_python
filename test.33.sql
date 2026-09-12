SELECT 
   flight_id,
   station,
   unload_time_minutes,
   NTILE(4) OVER(ORDER BY unload_time_minutes ASC) AS performance_quartile
FROM turnaround_times;


WITH ranked_delays AS(
    SELECT 
       Station,
       flight_date,
       DENSE_RANK() OVER(delay_minutes
    FROM station_delays;
) 

SELECT
  station, 
  flight_date,
  delay_minutes,
  ranked_delays
FROM ranked_delays
WHERE ranked_delays <=2;


WITH AS ranked_delays(
    SELECT 
      station,
      flight_date,
      DENSE_RANK() OVER(PARTITION BY station ORDER BY delay_minutes DESC) AS delay_min
FROM station_delays
)
SELECT 
   station,
   flight_date,
   delay_minutes,
   delay_min
FROM ranked_delays
WHERE ranked_delays <=2;


WITH agent_total AS(
    SELECT 
       agent_id,
       SUM(revenue) AS total_revenue,
       COUNT(sale_id) AS total_deals
   FROM cargo_sales
   GROUP BY agent_id
),
agent_rank AS (
    SELECT
       agent_id,
       total_revenue,
       total_deals,
    DENSE_RANK() OVER(ORDER BY total_revenue DESC) AS revenue_rank
    FROM agent_total
    WHERE total_deals > 1
)

SELECT 
   agent_id,
   total_revenue,
   total_deals,
   revenue_rank
FROM agent_rank;