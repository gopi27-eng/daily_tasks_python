import polars as pl
import pyarrow.dataset as ds
import duckdb
from loguru import logger
import os 


def quiy_the_data_lake():
    logger.info("---Creating Parquet File---")
    data = {
        "hub": ["Guwahati", "Delhi", "Guwahati", "Hyderabad", "Delhi"],
        "cargo_weight": [4500, 8000, 3200, 5600, 9000]
    }
    df = pl.DataFrame(data) 
    # Save it into praquet file
    df.write_parquet("cargo_lake.parquet")
    
    logger.info("--Pyarrow lazy scanner--")
    
    arrow_df = ds.dataset("cargo_lake.parquet", format = "parquet")
    
    logger.info("--SQL directily on Duckdb direct disk quiry--")
    
    sql_query = """SELECT 
                     hub ,SUM(cargo_weight) AS total_weight
                     FROM arrow_df 
                     GROUP BY hub;""" 
                     
    results = duckdb.sql(sql_query).pl()
    logger.success(f"\nFinal Aggregation:\n{results}")
    
    os.remove("cargo_lake.parquet")

if __name__ == "__main__":
    quiy_the_data_lake()