SELECT 
   f.flight_id, 
   f.route, 
   f.flight_date,
   p.name AS pilot_name
FROM flights f
INNER JOIN pilots P 
         ON f.pilot_id = p.pilot_id
LEFT JOIN cargo_manifests cm
         ON f.filght_id = cm.filght_id 
WHERE cm.flight_id IS NULL ;



SELECT 
   f1.pilot_id,
   f1.flight_date AS day_one_flight,
   f2.flight_date AS day_two_flight
FROM flights f1 
INNER JOIN flights f2 
      ON f1.pilot_id = f2.pilot_id 
      AND f2.flight_date = DATE_ADD(f1.flight_date, INTERVAL 1 DAY) ;




SELECT 
   p.pilot_id,
   p.name AS pilot_name,
   COALESCE(SUM(c.weight_kg),0) AS total_weight
FROM pilots p 
LEFT JOIN flights f 
   ON p.pilot_id = f.pilot_id 
LEFT JOIN cargo_manifests c 
   ON f.flight_id = c.flight_id   
GROUP BY p.pilot_id,p.name
ORDER BY total_weight DESC; 


SELECT
   p.name AS pilot_name,
   a.model AS aircraft_model,
   CASE 
      WHEN c.status IS NOT NULL THEN 'YES' 
      ELSE 'NO' 
   END AS is_certified
FROM pilots p
CROSS JOIN aircraft_types a
LEFT JOIN certifications c 
   ON p.pilot_id = c.pilot_id 
   AND a.type_id = c.type_id;


SELECT 
   p.name AS pilot_name,
   SUM(c.weight_kg) AS total_weight_kg
FROM pilots p
INNER JOIN flights f ON p.pilot_id = f.pilot_id 
INNER JOIN cargo_manifests c ON c.flight_id = f.flight_id 
WHERE f.status = 'COMPLETED'
GRoup BY p.name 
HAVING SUM(c.weight_kg) > 5000 
ORDER BY SUM(c.weight_kg) DESC; 


SELECT 
   a.registration_number
FROM aircraft a 
WHERE EXISTS(
   SELECT 1
   FROM maintenance_logs m
   WHERE a.aircraft_id = m.aircraft_id AND m.severity = 'CRITICAL'

);   

SELECT
   f.flight_id, 
   f.route, 
   f.total_weight_kg 
FROM flight_payloads f
WHERE f.total_weight_kg > (
   SELECT AVG(fp.total_weight_kg)
   FROM flight_payloads fp
)
ORDER BY f.total_weight_kg DESC;