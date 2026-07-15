import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Connection URL
db_url = os.getenv("DATABASE_URL", "sqlite:///sql_database/airline_analytics.db")

print(f"Connecting to database at: {db_url}")

# Ensure sql_database folder exists if SQLite is used
if db_url.startswith("sqlite:///"):
    sqlite_dir = os.path.dirname(db_url.replace("sqlite:///", ""))
    if sqlite_dir and not os.path.exists(sqlite_dir):
        os.makedirs(sqlite_dir)

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Database connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
    if "pymysql" in str(e) or "mysqlclient" in str(e):
        print("\n[NOTE] To connect to MySQL, you need a MySQL driver. You can install it with:")
        print("    pip install pymysql cryptography\n")
    print("Falling back to local SQLite database...")
    db_url = "sqlite:///sql_database/airline_analytics.db"
    os.makedirs("sql_database", exist_ok=True)
    engine = create_engine(db_url)

# Raw data file paths
raw_dir = r"c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\archive (5)\raw_data"
airports_list_path = os.path.join(raw_dir, "airports_list.csv")
coordinates_path = os.path.join(raw_dir, "AIRPORT_COORDINATES.csv")
carrier_decode_path = os.path.join(raw_dir, "CARRIER_DECODE.csv")
flights_path = os.path.join(raw_dir, "ONTIME_REPORTING_01.csv")
weather_path = os.path.join(raw_dir, "airport_weather_2019.csv")

# 1. Create Tables using schema.sql
print("Creating tables using schema.sql...")
schema_path = r"c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\sql_database\schema.sql"
with open(schema_path, "r") as f:
    schema_sql = f.read()

# Split schema statements
statements = schema_sql.split(";")
with engine.begin() as conn:
    if "mysql" in db_url:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for stmt in statements:
        cleaned_stmt = stmt.strip()
        if cleaned_stmt:
            conn.execute(text(cleaned_stmt))
    if "mysql" in db_url:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
print("Tables created successfully!")

# 2. Populate Delay Reasons Table
print("Populating delay_reasons table...")
delay_reasons_data = [
    {"reason_code": "CARRIER", "reason_description": "Carrier-controlled delay (e.g., maintenance, crew, cleaning)"},
    {"reason_code": "WEATHER", "reason_description": "Extreme weather conditions (e.g., storms, blizzards, hurricanes)"},
    {"reason_code": "NAS", "reason_description": "National Aviation System delay (e.g., air traffic control, heavy airport traffic)"},
    {"reason_code": "SECURITY", "reason_description": "Security delays (e.g., terminal evacuations, re-screening)"},
    {"reason_code": "LATE_AIRCRAFT", "reason_description": "Late arrival of previous flight using the same aircraft"},
    {"reason_code": "CANCEL_A", "reason_description": "Cancellation Code A: Carrier cancellation"},
    {"reason_code": "CANCEL_B", "reason_description": "Cancellation Code B: Weather cancellation"},
    {"reason_code": "CANCEL_C", "reason_description": "Cancellation Code C: National Aviation System cancellation"},
    {"reason_code": "CANCEL_D", "reason_description": "Cancellation Code D: Security cancellation"}
]
df_delay_reasons = pd.DataFrame(delay_reasons_data)

try:
    with engine.begin() as conn:
        if "mysql" in db_url:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("DELETE FROM delay_reasons"))
        if "mysql" in db_url:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
    df_delay_reasons.to_sql("delay_reasons", con=engine, if_exists="append", index=False)
    print("Delay reasons populated!")
except Exception as e:
    print(f"Error populating delay reasons: {e}")

# 3. Populate Airlines Table
print("Populating airlines table...")
try:
    df_carrier = pd.read_csv(carrier_decode_path)
    df_carrier = df_carrier.dropna(subset=["OP_UNIQUE_CARRIER", "CARRIER_NAME"])
    df_carrier = df_carrier.drop_duplicates(subset=["OP_UNIQUE_CARRIER"])
    df_carrier.columns = [col.lower() for col in df_carrier.columns]
    
    with engine.begin() as conn:
        if "mysql" in db_url:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("DELETE FROM airlines"))
        if "mysql" in db_url:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
    df_carrier.to_sql("airlines", con=engine, if_exists="append", index=False)
    print(f"Airlines populated! Total airlines: {len(df_carrier)}")
except Exception as e:
    print(f"Error populating airlines: {e}")

# 4. Populate Airports Table
print("Populating airports table...")
try:
    df_airports = pd.read_csv(airports_list_path)
    df_coords = pd.read_csv(coordinates_path)
    
    # Merge list and coordinates
    df_merged_airports = pd.merge(
        df_airports, 
        df_coords[['ORIGIN_AIRPORT_ID', 'LATITUDE', 'LONGITUDE']], 
        on='ORIGIN_AIRPORT_ID', 
        how='left'
    )
    
    df_merged_airports = df_merged_airports.dropna(subset=["ORIGIN_AIRPORT_ID"])
    df_merged_airports = df_merged_airports.drop_duplicates(subset=["ORIGIN_AIRPORT_ID"])
    df_merged_airports.columns = [col.lower() for col in df_merged_airports.columns]
    
    with engine.begin() as conn:
        if "mysql" in db_url:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("DELETE FROM airports"))
        if "mysql" in db_url:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
            
    df_merged_airports.to_sql("airports", con=engine, if_exists="append", index=False)
    print(f"Airports populated! Total airports: {len(df_merged_airports)}")
except Exception as e:
    print(f"Error populating airports: {e}")

# Load and prepare Weather Data
try:
    df_weather = pd.read_csv(weather_path, usecols=['NAME', 'DATE', 'PRCP', 'SNOW', 'SNWD', 'TMAX', 'AWND'])
    df_weather['date'] = pd.to_datetime(df_weather['DATE'], format='mixed')
    
    df_airports_list = pd.read_csv(airports_list_path)
    df_weather_mapped = pd.merge(df_weather, df_airports_list[['ORIGIN_AIRPORT_ID', 'NAME']], on='NAME', how='inner')
    df_weather_mapped = df_weather_mapped.drop_duplicates(subset=['ORIGIN_AIRPORT_ID', 'date'])
    print(f"Weather dataset loaded! Mapped stations: {df_weather_mapped['ORIGIN_AIRPORT_ID'].nunique()}")
except Exception as e:
    print(f"Warning: Failed to prepare weather data: {e}. Weather columns in flights will be NULL.")
    df_weather_mapped = None

# 5. Populate Flights Table (Sample of 50k rows to keep database size optimal and fast)
print("Populating flights table...")
try:
    chunk_size = 10000
    sample_flights = []
    target_count = 50000
    
    for chunk in pd.read_csv(flights_path, chunksize=chunk_size):
        chunk = chunk.dropna(subset=['OP_UNIQUE_CARRIER', 'ORIGIN_AIRPORT_ID', 'DEST_AIRPORT_ID'])
        
        # Filter constraints
        chunk = chunk[chunk['OP_UNIQUE_CARRIER'].isin(df_carrier['op_unique_carrier'])]
        chunk = chunk[chunk['ORIGIN_AIRPORT_ID'].isin(df_merged_airports['origin_airport_id'])]
        chunk = chunk[chunk['DEST_AIRPORT_ID'].isin(df_merged_airports['origin_airport_id'])]
        
        # Construct date for joining weather
        chunk['date'] = pd.to_datetime('2019-' + chunk['MONTH'].astype(str) + '-' + chunk['DAY_OF_MONTH'].astype(str), format='mixed')
        
        # Join Weather columns if mapped
        if df_weather_mapped is not None:
            chunk = pd.merge(
                chunk, 
                df_weather_mapped[['ORIGIN_AIRPORT_ID', 'date', 'PRCP', 'SNOW', 'SNWD', 'TMAX', 'AWND']], 
                on=['ORIGIN_AIRPORT_ID', 'date'], 
                how='left'
            )
            
        sample_flights.append(chunk)
        current_total = sum(len(c) for c in sample_flights)
        if current_total >= target_count:
            break
            
    df_flights = pd.concat(sample_flights).head(target_count)
    
    # Drop date column as it's not in flights schema
    if 'date' in df_flights.columns:
        df_flights = df_flights.drop(columns=['date'])
        
    if 'Unnamed: 32' in df_flights.columns:
        df_flights = df_flights.drop(columns=['Unnamed: 32'])
    
    df_flights.columns = [col.lower() for col in df_flights.columns]
    df_flights = df_flights.replace({np.nan: None})
    
    # SQLite/MySQL PK Auto-Increment handling
    if "flight_id" in df_flights.columns:
        df_flights = df_flights.drop(columns=["flight_id"])

    with engine.begin() as conn:
        if "mysql" in db_url:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("DELETE FROM flights"))
        if "mysql" in db_url:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        
    df_flights.to_sql("flights", con=engine, if_exists="append", index=False, chunksize=5000)
    print(f"Flights table populated! Total seeded flights: {len(df_flights)}")
    
    # Check data count
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM flights")).scalar()
        print(f"Verified flight records count in DB: {result}")
        
except Exception as e:
    print(f"Error populating flights: {e}")

print("\nData ingestion pipeline complete!")
