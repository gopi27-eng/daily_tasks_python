import polars as pl
import duckdb

def analyze_cargo_next_gen():
    print("---Polars & duckDB intigration---")
    
    data = {
        "flight_number": ["QJ-101", "QJ-101", "QJ-205", "QJ-205", "QJ-309"],
        "weight_kg": [4500, 1200, 8900, 500, 5000]
    }
    df = pl.DataFrame(data)
    print("\nduckdb SQL quiry:")
    aggrigated_df = duckdb.sql("""SELECT flight_number, SUM(weight_kg) AS total_weight
        FROM df
        GROUP BY flight_number""")
    print(aggrigated_df)
    
    
analyze_cargo_next_gen()