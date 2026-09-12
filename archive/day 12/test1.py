from pydantic import BaseModel, ValidationError
import pandera as pa
from pandera.typing import Series
import pandas as pd
from logging_utils.log import setup_logger

logger = setup_logger("log_test.log")

class FlightRecord(BaseModel):
    flight_id: str
    weight_kg: float
    status: str

class FlightSchema(pa.SchemaModel):
    flight_id: Series[str] = pa.Field(str_startswith="QJ-")
    weight_kg: Series[float] = pa.Field(ge=0)
    status: Series[str] = pa.Field(isin=["ON_TIME", "DELAY"])

def enforce_contracts():
    logger.info("--- Booting Data Quality Engine ---")
    
    raw_api_data = [
        {"flight_id": "QJ-101", "weight_kg": 4500, "status": "ON_TIME"},
        {"flight_id": "XX-999", "weight_kg": 5000, "status": "DELAY"},   # Pandera fail
        {"flight_id": "QJ-205", "weight_kg": -100, "status": "ON_TIME"}, # Pandera fail
        {"flight_id": "QJ-309", "weight_kg": "missing", "status": "CRASHED"} # Pydantic fail
    ]
    
    valid_records = []
    
    for record in raw_api_data:
        try:
            parsed = FlightRecord(**record)
            valid_records.append(parsed.model_dump())
        except ValidationError:
            logger.error(f"Pydantic blocked bad row: {record}")
            
    df = pd.DataFrame(valid_records)
    
    try:
        validated_df = FlightSchema.validate(df)
        logger.success(f"Final Data Warehouse Ready:\n{validated_df}")
    except pa.errors.SchemaError as e:
        logger.error(f"Pandera caught a schema violation:\n{e.failure_cases}")

if __name__ == "__main__":
    enforce_contracts()
