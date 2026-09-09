import polars as pl
import dask.dataframe as dd
from loguru import logger

def dask_pipeline():
    logger.info("--Dask pipeline started--")
    
    # 1. Create Polars DataFrame
    data = {
        "flight": ["QJ-101", "QJ-205", "QJ-101", "QJ-309"] * 100000, 
        "payload": [4000, 5000, 4500, 3000] * 100000
    }
    pl_df = pl.DataFrame(data)
    logger.info("--Polars DataFrame created--")
    
    # 2. Convert Polars → Pandas → Dask
    pandas_df = pl_df.to_pandas()
    dask_df = dd.from_pandas(pandas_df, npartitions=8)
    
    # 3. Aggregation logic (Average payload per flight)
    avg_payload = dask_df.groupby("flight")["payload"].mean()
    logger.info("Lazy Dask Object (No data processed yet):")
    print(avg_payload)
    
    # 4. Trigger computation
    result = avg_payload.compute()
    logger.success("Final Computed Result:")
    print(result)

if __name__ == "__main__":
    dask_pipeline()
