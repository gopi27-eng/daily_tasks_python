import fakeredis
from sqlalchemy import create_engine, text
from logging_utils.log import setup_logger

logger = setup_logger("sql_pipeline.log")

db_engine = create_engine("sqlite:///:memory:")

with db_engine.connect() as conn:
    conn.execute(text("CREATE TABLE flights (flight_id TEXT PRIMARY KEY, status TEXT);"))
    conn.execute(text("INSERT INTO flights (flight_id, status) VALUES ('QJ-101', 'ON_TIME'), ('QJ-205', 'DELAY');"))
    conn.commit()
    
redis_client = fakeredis.FakeRedis(decode_responses=True)

def flight_status(flight_id: str):
    logger.info(f"Fetching status for {flight_id}...")
    
    # 1. Check Cache First
    check_status = redis_client.get(flight_id)
    if check_status:
        logger.success(f"Cache HIT: retrieved {check_status} from Redis")
        return check_status
        
    logger.warning("Cache MISS: Data not found in Redis, querying SQLite.")
    
    # 2. Fallback to SQL Database
    with db_engine.connect() as conn:
        query = text("SELECT status FROM flights WHERE flight_id = :fid")
        result = conn.execute(query, {"fid": flight_id}).scalar()
        
    # 3. Write Back to Cache
    if result:
        redis_client.set(flight_id, result, ex=60)
        
    return result

if __name__ == "__main__":
    # Test 1: Queries DB (Cache Miss)
    flight_status('QJ-101')
    
    # Test 2: Instant lookup (Cache Hit)
    flight_status('QJ-101')