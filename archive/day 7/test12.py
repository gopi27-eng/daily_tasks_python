import polars as pl
import pyarrow as pa
import duckdb 
from loguru import logger


def the_arrow_brigde():
    logger.info("\n--polars --> pyarrow--> duckdb--> polars")
    
    flights_pl = pl.DataFrame({
        "flight_id": ["QJ-101", "QJ-205", "QJ-309", "QJ-404"],
        "delay_mins": [15, 0, 45, 120]
    })
    pl_df = pl.DataFrame(flights_pl)
    logger.info(f"Raw data successfully coverted to polars {pl_df}")
    
    logger.info("---polars to pyarrow conversions for in memory ---")
    pa_df = pl_df.to_arrow()
    
    logger.info("---duckdb SQL quiry---")
    
    results = duckdb.sql("""
                         SELECT 
                            flight_id,
                            delay_mins,
                            CASE 
                               WHEN delay_mins > 0 THEN 'DELAY' 
                               ELSE 'ON_TIME' 
                            END AS STATUS 
                        FROM pa_df;
                         """)
    final_df = results.pl()
    logger.info(f"\nFinal Result (Back in Polars): {final_df}")
    

if __name__ == "__main__":
    the_arrow_brigde()