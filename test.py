import pymongo
import boto3
from loguru import logger
from pathlib import Path

# Mock data simulating the output of your async scraper
cargo_payloads = [
    {"flight": "QJ-101", "hub": "Guwahati", "status": "ON_TIME"},
    {"flight": "QJ-205", "hub": "Delhi", "status": "DELAY"},
    {"flight": "QJ-309", "hub": "Hyderabad", "status": "ON_TIME"}
]

# Create a dummy log file to upload
log_file = Path("pipeline.log")
log_file.write_text("ETL Run Successful at 02:00 AM")

def load_to_mongo(data: list):
    logger.info("--- Connecting to MongoDB Atlas ---")
    
    # 1. Initialize the MongoClient (using a mock connection string)
    client = pymongo.MongoClient("mongodb+srv://admin:mock_pass@cluster0.mongodb.net/")
    db = client["qj-docdb"]
    
    collections = db["live-rout-server"]
    result = collections.insert_many(data)
    logger.success(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")

def backup_to_s3(file_path: Path):
    logger.info("--- Connecting to AWS S3 ---")
    
    # 4. Initialize the boto3 S3 client
    s3 = boto3.client('s3', region_name='ap-south-1')
    
    # 5. Upload the file to S3
    s3.upload_file(Filename=str(file_path), Bucket="quikjet-datalake-prod", Key=file_path.name)
    logger.success(f"Backed up {file_path.name} to AWS S3.")

if __name__ == "__main__":
    load_to_mongo(cargo_payloads)
    backup_to_s3(log_file)
    
    # Cleanup dummy file
    if log_file.exists():
        log_file.unlink()
