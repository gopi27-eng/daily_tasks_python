SELECT 
   manifest_id,
   category,
   weight_kg,
  DENSE_RANK()OVER(PARTITION BY weight_kg ASC) AS weight_rank
FROM cargo_shipments;
