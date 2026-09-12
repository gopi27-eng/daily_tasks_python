SELECT 
   manifest_id,
   category,
   weight_kg,
  DENSE_RANK()OVER(PARTITION BY category ORDER BY weight_kg DESC) AS weight_rank
FROM cargo_shipments;
SELECT 
   manifest_id,
   category,
   weight_kg,
  DENSE_RANK()OVER(PARTITION BY category ORDER BY weight_kg DESC) AS weight_kg
FROM cargo_shipments;



SELECT 
   flight_id,
   pilot_id,
   departure_time,
   LAG(departure_time) OVER(PARTITION BY pilot_id ORDER BY departure_time ASC) AS previous_departure_time
FROM pilot_flights;

SELECT
   handler_team,
   load_date,
   weight_kg,
   SUM(weight_kg) OVER(PARTITION BY handler_team ORDER BY load_date ASC) AS cumulative_weight_kg
FROM daily_cargo_loads;