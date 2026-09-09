SELECT 
   f.flight_number, 
   f.route_destination,
   COALESCE(SUM(cs.weight_kg), 0) AS total_cargo_weight
CASE
   WHEN SUM(cs.weight_kg) = 0 THEN 'GHOST FLIGHT'
   ELSE 'ACTIVE FLIGHT'
END AS flight_status
FROM flights AS f
LEFT JOIN cargo_shipments AS cs ON f.flight_number = cs.flight_number
GROUP BY f.flight_number, f.route_destination;

SELECT 
    flight_id,
    weight_kg,
    CASE 
        WHEN weight_kg > (SELECT AVG(weight_kg) FROM cargo_shipments) THEN 'Heavyweight'
        ELSE 'Normal'
    END AS is_above_average
FROM cargo_shipments;