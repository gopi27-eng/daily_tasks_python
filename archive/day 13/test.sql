SELECT 
aircraft_reg,
flight_date,
fuel_burned_kg,
AVG(fuel_burned_kg) OVER(PARTITION BY aircraft_reg ORDER BY flight_date ASC ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
  AS rolling_3_day_avg
FROM daily_fuel_burn;