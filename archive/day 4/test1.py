import pandas as pd

# 1. The Flights Data
flights_data = {
    'flight_id': [1, 2, 3, 4],
    'flight_number': ['QJ-101', 'QJ-205', 'QJ-309', 'QJ-404'],
    'route_destination': ['Guwahati', 'Delhi', 'Guwahati', 'Kolkata']
}
df_flights = pd.DataFrame(flights_data)

# 2. The Cargo Data
cargo_data = {
    'shipment_id': [1001, 1002, 1003, 1004],
    'flight_id': [1, 1, 2, 3],
    'weight_kg': [4500.50, 1200.00, 8900.75, 3400.00]
}
df_cargo = pd.DataFrame(cargo_data)


df_merged = pd.merge(df_flights, df_cargo, on='flight_id', how='left')
print(df_merged) 

df_ghost = df_merged[df_merged['shipment_id'].isna()]
print(df_ghost)


df_payload = df_merged.groupby("route_destination")["weight_kg"].sum()
print(df_payload)