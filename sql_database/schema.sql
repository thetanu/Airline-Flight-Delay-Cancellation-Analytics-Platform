-- Airline Flight Delay & Cancellation Database Schema
-- Compatible with MySQL and SQLite (via SQLAlchemy)

-- Clean up existing tables to avoid duplicate index or primary key issues on re-run
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS airports;
DROP TABLE IF EXISTS airlines;
DROP TABLE IF EXISTS delay_reasons;

-- 1. Airports Table
CREATE TABLE IF NOT EXISTS airports (
    origin_airport_id INT PRIMARY KEY,
    display_airport_name VARCHAR(255) NOT NULL,
    origin_city_name VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

-- 2. Airlines Table
CREATE TABLE IF NOT EXISTS airlines (
    airline_id INT,
    op_unique_carrier VARCHAR(10) PRIMARY KEY,
    carrier_name VARCHAR(255) NOT NULL
);

-- 3. Delay Reasons Table
CREATE TABLE IF NOT EXISTS delay_reasons (
    reason_code VARCHAR(20) PRIMARY KEY,
    reason_description VARCHAR(255) NOT NULL
);

-- 4. Flights Table
CREATE TABLE IF NOT EXISTS flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    month INT NOT NULL,
    day_of_month INT NOT NULL,
    day_of_week INT NOT NULL,
    op_unique_carrier VARCHAR(10) NOT NULL,
    tail_num VARCHAR(20),
    op_carrier_fl_num INT NOT NULL,
    origin_airport_id INT NOT NULL,
    origin VARCHAR(10) NOT NULL,
    origin_city_name VARCHAR(255) NOT NULL,
    dest_airport_id INT NOT NULL,
    dest VARCHAR(10) NOT NULL,
    dest_city_name VARCHAR(255) NOT NULL,
    crs_dep_time INT NOT NULL,
    dep_time INT,
    dep_delay_new FLOAT DEFAULT 0.0,
    dep_del15 FLOAT DEFAULT 0.0,
    dep_time_blk VARCHAR(20),
    crs_arr_time INT NOT NULL,
    arr_time INT,
    arr_delay_new FLOAT DEFAULT 0.0,
    arr_time_blk VARCHAR(20),
    cancelled FLOAT DEFAULT 0.0,
    cancellation_code VARCHAR(5),
    crs_elapsed_time FLOAT,
    actual_elapsed_time FLOAT,
    distance FLOAT,
    distance_group INT,
    carrier_delay FLOAT DEFAULT 0.0,
    weather_delay FLOAT DEFAULT 0.0,
    nas_delay FLOAT DEFAULT 0.0,
    security_delay FLOAT DEFAULT 0.0,
    late_aircraft_delay FLOAT DEFAULT 0.0,
    
    -- Weather conditions joined from NOAA datasets
    prcp FLOAT DEFAULT 0.0,
    snow FLOAT DEFAULT 0.0,
    snwd FLOAT DEFAULT 0.0,
    tmax FLOAT,
    awnd FLOAT,
    
    FOREIGN KEY (origin_airport_id) REFERENCES airports(origin_airport_id),
    FOREIGN KEY (dest_airport_id) REFERENCES airports(origin_airport_id),
    FOREIGN KEY (op_unique_carrier) REFERENCES airlines(op_unique_carrier)
);

-- Indexes for performance tuning and faster analytics queries
CREATE INDEX idx_flights_origin_airport ON flights(origin_airport_id);
CREATE INDEX idx_flights_dest_airport ON flights(dest_airport_id);
CREATE INDEX idx_flights_carrier ON flights(op_unique_carrier);
CREATE INDEX idx_flights_month ON flights(month);
CREATE INDEX idx_flights_dep_del15 ON flights(dep_del15);
CREATE INDEX idx_flights_cancelled ON flights(cancelled);
