import sys
import typer
import httpx
import duckdb
import polars as pl
from loguru import logger
from pathlib import Path
from omegaconf import OmegaConf

app = typer.Typer() 

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR/"logs"/ "pipeline.log"
OUTPUT_DIR = BASE_DIR/"output"

logger.add(
    LOG_DIR,
    rotation = "10 MB",
    retention = "7 days",
    compression = "zip",
    level = "INFO",
    format = "{time: YYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

def checK_helath_network():
    
    logger.info("Checking network health...")
    try:
        response = httpx.get("https://httpbin.org/status/200")
        if not response.status_code == 200:
            logger.error("hitting error staus_code:{response.status_code}")
            sys.exit(1)
        pass 
    except httpx.RequestError as e:
        logger.error(f"Network down: {e}")
        sys.exit(1)
@app.command()       
def run_etl():
    """Main ETL Pipeline Command"""
    logger.info("--- Booting Cargo Engine ---")
    
    checK_helath_network()
   
    config =  OmegaConf.load(BASE_DIR/"config.yaml")
    min_weight = config.filters.min_weight_kg
    logger.info("--ingesting data into polars--")
    pl_df = pl.DataFrame({
        "flight_id": ["QJ-101", "QJ-205", "QJ-309", "QJ-404", "QJ-505"]*10000,
        "hub": ["Guwahati", "Delhi", "Hyderabad", "Guwahati", "Delhi"]*10000,
        "weight_kg": [4500, 3200, 8900, 1500, 5000]*10000,
        "status": ["ON_TIME", "DELAY", "ON_TIME", "ON_TIME", "DELAY"]*10000
    })
       
    logger.info("Running Duckdb SQLtransformation...") 
    
    sql_query = f"""
              SELECT * 
              FROM pl_df
              WHERE weight_kg > {min_weight} 
              """ 
    
    results = duckdb.sql(sql_query)
    
    logger.info("Successfully SQL query done!")
    
    transofrmed_pl_df = results.pl()
    logger.info(f"Saving {len(transofrmed_pl_df)} records to Parquet...") 
    
    
    OUTPUT_DIR.mkdir(parents= True, exist_ok=True)
    OUTPUT_FILE = OUTPUT_DIR/"output.parquet"
    transofrmed_pl_df.write_parquet(OUTPUT_FILE)
    
    logger.success("ETL Pipeline completed perfectly.")
    
if __name__ == "__main__":
    app()