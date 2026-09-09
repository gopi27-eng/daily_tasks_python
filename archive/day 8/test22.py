import ray
import time
from loguru import logger

# 1. Initialize Ray cluster
ray.init()

# 2. Add the Ray decorator to make this a distributed task
@ray.remote
def process_flight(flight_id):
    time.sleep(1) # Simulating a heavy ML inference task
    return f"{flight_id} ML processing complete."

def run_ray_pipeline():
    logger.info("--- Starting Ray Distributed Engine ---")
    start_time = time.time()
    
    flights = ["QJ-101", "QJ-205", "QJ-309"]
    
    # 3. Trigger the function concurrently using .remote()
    futures = [process_flight.remote(f) for f in flights]
    
    # 4. Collect the results using ray.get()
    results = ray.get(futures)
    
    logger.success(f"Results: {results}")
    logger.info(f"Total Execution Time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    run_ray_pipeline()