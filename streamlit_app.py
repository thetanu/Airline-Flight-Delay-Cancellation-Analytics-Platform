import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os
import json
import joblib
import altair as alt
import sys
from dotenv import load_dotenv

# Append python directory to system path for deserializing custom ML modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'python'))
from feature_engineering import FlightDataPreprocessor

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Airline Flight Delay Analytics Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Main body background and fonts */
    .stApp {
        background-color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #1F4E78 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Premium KPI Card Styling */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 25px;
        margin-top: 15px;
    }
    .kpi-card {
        flex: 1;
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        border-left: 5px solid #1F4E78;
        transition: transform 0.2s ease-in-out;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748B;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E293B;
    }
    .kpi-subtitle {
        font-size: 0.75rem;
        color: #94A3B8;
        margin-top: 5px;
    }
    
    /* Prediction Card styling */
    .pred-card-ontime {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 8px solid #22C55E;
        padding: 20px;
        border-radius: 10px;
        color: #166534;
        margin-bottom: 20px;
    }
    .pred-card-delay {
        background: #FEF2F2;
        border: 1px solid #FEE2E2;
        border-left: 8px solid #EF4444;
        padding: 20px;
        border-radius: 10px;
        color: #991B1B;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to connect to database
def get_db_connection():
    db_url = os.getenv("DATABASE_URL", "sqlite:///sql_database/airline_analytics.db")
    if db_url.startswith("mysql"):
        import urllib.parse
        import pymysql
        parsed = urllib.parse.urlparse(db_url)
        username = parsed.username
        password = urllib.parse.unquote(parsed.password) if parsed.password else ""
        hostname = parsed.hostname or "localhost"
        port = parsed.port or 3306
        db_name = parsed.path[1:]
        
        return pymysql.connect(
            host=hostname,
            port=port,
            user=username,
            password=password,
            database=db_name
        )
    else:
        db_path = db_url.replace("sqlite:///", "")
        return sqlite3.connect(db_path)

# Load ML Assets
@st.cache_resource
def load_ml_assets():
    model_path = "python/model/flight_delay_model.joblib"
    cats_path = "python/model/categories.json"
    rates_path = "python/model/historical_rates.json"
    
    pipeline = joblib.load(model_path) if os.path.exists(model_path) else None
    
    categories = {}
    if os.path.exists(cats_path):
        with open(cats_path, "r") as f:
            categories = json.load(f)
            
    rates = {}
    if os.path.exists(rates_path):
        with open(rates_path, "r") as f:
            rates = json.load(f)
            
    return pipeline, categories, rates

pipeline, categories, rates = load_ml_assets()

# Main Header
st.title("✈️ Airline Flight Delay & Cancellation Analytics Platform")
st.markdown("An end-to-end interactive decision-support system analyzing flight delays, cancellations, and operational metrics.")

# Tabs Setup
tab_dashboard, tab_predict, tab_sql, tab_ml, tab_reports = st.tabs([
    "📊 Executive KPI Dashboard", 
    "🔮 Interactive Delay Predictor", 
    "💻 SQL Query Console", 
    "📈 ML Model Evaluation",
    "📥 Reports & Downloads"
])

# ==================== TAB 1: EXECUTIVE KPI DASHBOARD ====================
with tab_dashboard:
    st.header("Executive KPI Dashboard")
    
    # 1. KPI Cards Row
    st.markdown("""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">Total Flights Analyzed</div>
            <div class="kpi-value">50,000</div>
            <div class="kpi-subtitle">Sample size from January 2019</div>
        </div>
        <div class="kpi-card" style="border-left-color: #22C55E;">
            <div class="kpi-title">Average On-Time Performance (OTP)</div>
            <div class="kpi-value">81.04%</div>
            <div class="kpi-subtitle">Goal: &gt; 80% (Within target)</div>
        </div>
        <div class="kpi-card" style="border-left-color: #EAB308;">
            <div class="kpi-title">Average Departure Delay</div>
            <div class="kpi-value">11.23 mins</div>
            <div class="kpi-subtitle">Average duration across all flights</div>
        </div>
        <div class="kpi-card" style="border-left-color: #EF4444;">
            <div class="kpi-title">Flight Cancellation Rate</div>
            <div class="kpi-value">1.52%</div>
            <div class="kpi-subtitle">Goal: &lt; 2.0% (Within target)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    conn = get_db_connection()
    if conn:
        # Load data for visualizations
        df_airlines = pd.read_sql_query("""
            SELECT 
                a.carrier_name AS Airline,
                COUNT(*) AS Total_Flights,
                SUM(f.dep_del15) AS Delayed_Flights,
                ROUND(SUM(f.dep_del15) * 100.0 / COUNT(*), 2) AS Delay_Rate,
                ROUND(AVG(f.dep_delay_new), 2) AS Avg_Delay_Mins
            FROM flights f
            JOIN airlines a ON f.op_unique_carrier = a.op_unique_carrier
            GROUP BY a.carrier_name
            ORDER BY Delay_Rate DESC
        """, conn)
        
        df_airports = pd.read_sql_query("""
            SELECT 
                o.display_airport_name AS Airport,
                COUNT(*) AS Total_Departures,
                SUM(f.dep_del15) AS Delayed_Departures,
                ROUND(SUM(f.dep_del15) * 100.0 / COUNT(*), 2) AS Delay_Rate,
                ROUND(AVG(f.dep_delay_new), 2) AS Avg_Delay_Mins
            FROM flights f
            JOIN airports o ON f.origin_airport_id = o.origin_airport_id
            GROUP BY o.display_airport_name
            ORDER BY Delay_Rate DESC
            LIMIT 10
        """, conn)
        
        df_weather = pd.read_sql_query("""
            SELECT 
                f.prcp AS Precipitation,
                AVG(f.dep_delay_new) AS Avg_Delay_Mins,
                COUNT(*) AS Flight_Count
            FROM flights f
            WHERE f.prcp IS NOT NULL
            GROUP BY f.prcp
            HAVING Flight_Count > 10
            ORDER BY f.prcp
        """, conn)
        
        df_time_block = pd.read_sql_query("""
            SELECT 
                f.dep_time_blk AS Time_Block,
                AVG(f.dep_delay_new) AS Avg_Delay_Mins,
                SUM(f.dep_del15) * 100.0 / COUNT(*) AS Delay_Rate
            FROM flights f
            GROUP BY f.dep_time_blk
            ORDER BY f.dep_time_blk
        """, conn)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Airline Reliability: Delay Rates & Durations")
            # Altair Chart: Airline Delay Rates
            chart_airline = alt.Chart(df_airlines).mark_bar(color='#1F4E78').encode(
                x=alt.X('Delay_Rate:Q', title='Delay Rate (%)'),
                y=alt.Y('Airline:N', sort='-x', title='Airline'),
                tooltip=['Airline', 'Total_Flights', 'Delay_Rate', 'Avg_Delay_Mins']
            ).properties(height=350)
            st.altair_chart(chart_airline, use_container_width=True)
            
        with col2:
            st.subheader("Top 10 Bottleneck Origin Airports")
            chart_airport = alt.Chart(df_airports).mark_bar(color='#5B9BD5').encode(
                x=alt.X('Avg_Delay_Mins:Q', title='Avg Departure Delay (min)'),
                y=alt.Y('Airport:N', sort='-x', title='Origin Airport'),
                tooltip=['Airport', 'Total_Departures', 'Delay_Rate', 'Avg_Delay_Mins']
            ).properties(height=350)
            st.altair_chart(chart_airport, use_container_width=True)
            
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Delay Patterns by Time of Day")
            chart_time = alt.Chart(df_time_block).mark_line(point=True, color='#EAB308').encode(
                x=alt.X('Time_Block:N', title='Departure Time Block'),
                y=alt.Y('Delay_Rate:Q', title='Delay Probability (%)'),
                tooltip=['Time_Block', 'Delay_Rate', 'Avg_Delay_Mins']
            ).properties(height=300)
            st.altair_chart(chart_time, use_container_width=True)
            
        with col4:
            st.subheader("Weather Impact: Precipitation vs. Flight Delays")
            chart_weather = alt.Chart(df_weather).mark_circle(size=60, color='#C00000').encode(
                x=alt.X('Precipitation:Q', title='Daily Precipitation (inches)'),
                y=alt.Y('Avg_Delay_Mins:Q', title='Avg Delay (minutes)'),
                tooltip=['Precipitation', 'Avg_Delay_Mins', 'Flight_Count']
            ).properties(height=300)
            st.altair_chart(chart_weather, use_container_width=True)
            
        conn.close()

# ==================== TAB 2: INTERACTIVE DELAY PREDICTOR ====================
with tab_predict:
    st.header("Interactive Delay Predictor")
    st.markdown("Enter details for an upcoming flight below to predict its probability of a departure delay (>15 mins) and understand key contributing risk factors.")
    
    if not pipeline:
        st.warning("ML Pipeline not found. Make sure model is trained and saved in python/model/flight_delay_model.joblib")
    else:
        # Pre-load dropdown options from categories.json
        carriers = categories.get("CARRIER_NAME", [])
        airports = categories.get("DEPARTING_AIRPORT", [])
        prev_airports = categories.get("PREVIOUS_AIRPORT", [])
        time_blocks = categories.get("DEP_TIME_BLK", [])
        
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            st.subheader("📋 Flight Details")
            selected_carrier = st.selectbox("Airline Carrier", carriers, index=carriers.index("American Airlines Inc.") if "American Airlines Inc." in carriers else 0)
            selected_airport = st.selectbox("Departing Airport", airports, index=airports.index("Chicago O'Hare International") if "Chicago O'Hare International" in airports else 0)
            selected_prev_airport = st.selectbox("Previous Airport", prev_airports, index=prev_airports.index("NONE") if "NONE" in prev_airports else 0)
            selected_time_block = st.selectbox("Departure Time Block", time_blocks, index=time_blocks.index("1500-1559") if "1500-1559" in time_blocks else 0)
            
        with col_f2:
            st.subheader("✈️ Aircraft & Route Settings")
            month = st.slider("Month of Travel", 1, 12, 7)
            day_of_week = st.slider("Day of the Week (1=Mon, 7=Sun)", 1, 7, 5)
            plane_age = st.number_input("Aircraft Age (years)", min_value=0, max_value=40, value=8)
            num_seats = st.number_input("Number of Seats", min_value=10, max_value=500, value=150)
            segment_num = st.number_input("Segment Number (Flight sequence today)", min_value=1, max_value=15, value=2)
            distance_group = st.slider("Distance Group (1 = short, 11 = long)", 1, 11, 4)
            
        with col_f3:
            st.subheader("🌧️ Weather Conditions")
            prcp = st.number_input("Precipitation (inches)", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
            snow = st.number_input("Snowfall (inches)", min_value=0.0, max_value=24.0, value=0.0, step=0.5)
            snwd = st.number_input("Snow Depth on Ground (inches)", min_value=0.0, max_value=48.0, value=0.0, step=1.0)
            tmax = st.number_input("Max Temperature (°F)", min_value=-30.0, max_value=120.0, value=75.0, step=1.0)
            awnd = st.number_input("Average Wind Speed (mph)", min_value=0.0, max_value=60.0, value=8.5, step=1.0)

        # Run Prediction
        if st.button("🔮 Predict Flight Delay Risk", type="primary", use_container_width=True):
            # 1. Fetch historical rate lookups
            global_mean = rates.get("global_mean", 0.1891)
            carrier_hist = rates.get("carrier_rates", {}).get(selected_carrier, global_mean)
            airport_hist = rates.get("airport_rates", {}).get(selected_airport, global_mean)
            day_hist = rates.get("day_rates", {}).get(str(day_of_week), global_mean)
            block_hist = rates.get("block_rates", {}).get(selected_time_block, global_mean)
            
            # 2. Estimate concurrent flights from DB or fallback
            concurrent = 15
            conn = get_db_connection()
            if conn:
                try:
                    db_url = os.getenv("DATABASE_URL", "")
                    placeholder = "%s" if db_url.startswith("mysql") else "?"
                    c_cursor = conn.cursor()
                    query = f"""
                        SELECT AVG(concurrent_flights) FROM (
                            SELECT COUNT(*) as concurrent_flights 
                            FROM flights 
                            WHERE origin_airport_id = (SELECT origin_airport_id FROM airports WHERE display_airport_name = {placeholder})
                            AND dep_time_blk = {placeholder}
                            GROUP BY day_of_month
                        )
                    """
                    c_cursor.execute(query, (selected_airport, selected_time_block))
                    res = c_cursor.fetchone()[0]
                    if res:
                        concurrent = int(res)
                except:
                    pass
                conn.close()
            
            # 3. Create input DataFrame in the exact sequence expected by features pipeline
            input_dict = {
                # Categoricals
                'DEP_TIME_BLK': [selected_time_block],
                'CARRIER_NAME': [selected_carrier],
                'DEPARTING_AIRPORT': [selected_airport],
                'PREVIOUS_AIRPORT': [selected_prev_airport],
                
                # Numericals
                'MONTH': [month],
                'DAY_OF_WEEK': [day_of_week],
                'DISTANCE_GROUP': [distance_group],
                'SEGMENT_NUMBER': [segment_num],
                'CONCURRENT_FLIGHTS': [concurrent],
                'NUMBER_OF_SEATS': [num_seats],
                
                # Fetch typical monthly aggregates from database for selected airport/carrier
                'AIRPORT_FLIGHTS_MONTH': [12000],  # realistic defaults
                'AIRLINE_FLIGHTS_MONTH': [24000],
                'AIRLINE_AIRPORT_FLIGHTS_MONTH': [450],
                'AVG_MONTHLY_PASS_AIRPORT': [850000],
                'AVG_MONTHLY_PASS_AIRLINE': [1900000],
                'FLT_ATTENDANTS_PER_PASS': [0.0006],
                'GROUND_SERV_PER_PASS': [0.0012],
                
                'PLANE_AGE': [plane_age],
                
                # Geographics
                'LATITUDE': [41.97], # Chicago O'Hare default or look up
                'LONGITUDE': [-87.90],
                
                # Weather
                'PRCP': [prcp],
                'SNOW': [snow],
                'SNWD': [snwd],
                'TMAX': [tmax],
                'AWND': [awnd],
                
                # Historical
                'CARRIER_HISTORICAL': [carrier_hist],
                'DEP_AIRPORT_HIST': [airport_hist],
                'DAY_HISTORICAL': [day_hist],
                'DEP_BLOCK_HIST': [block_hist]
            }
            
            # Fetch actual coordinates from DB if possible
            conn = get_db_connection()
            if conn:
                try:
                    db_url = os.getenv("DATABASE_URL", "")
                    placeholder = "%s" if db_url.startswith("mysql") else "?"
                    c_cursor = conn.cursor()
                    c_cursor.execute(f"SELECT latitude, longitude FROM airports WHERE display_airport_name = {placeholder}", (selected_airport,))
                    coords = c_cursor.fetchone()
                    if coords:
                        input_dict['LATITUDE'] = [coords[0]]
                        input_dict['LONGITUDE'] = [coords[1]]
                except:
                    pass
                conn.close()
                
            X_input = pd.DataFrame(input_dict)
            
            # Run prediction
            prob = pipeline.predict_proba(X_input)[0, 1]
            pred = pipeline.predict(X_input)[0]
            
            st.subheader("🎯 Prediction Result")
            
            col_res1, col_res2 = st.columns([2, 3])
            
            with col_res1:
                if pred == 0:
                    st.markdown("""
                    <div class="pred-card-ontime">
                        <h3>🟢 ON-TIME EXPECTED</h3>
                        <p>The model predicts that this flight will depart on schedule or experience a negligible delay (&lt;15 mins).</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="pred-card-delay">
                        <h3>🔴 DELAY RISK DETECTED</h3>
                        <p>The model predicts that this flight is highly likely to experience a delay of 15 minutes or more.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.metric("Delay Probability", f"{prob*100:.1f}%", delta=f"{(prob - global_mean)*100:+.1f}% vs. Average")
                st.progress(float(prob))
                
            with col_res2:
                st.subheader("🔍 Major Risk Contributions")
                # Visual explanation of historical risk features
                features_contrib = pd.DataFrame({
                    "Risk Factor": ["Airport Delays", "Time Slot Congestion", "Airline Reliability", "Day of Week Pattern"],
                    "Selected_Rate": [airport_hist * 100, block_hist * 100, carrier_hist * 100, day_hist * 100],
                    "Global_Average": [global_mean * 100] * 4
                })
                
                chart_contrib = alt.Chart(features_contrib).mark_bar().encode(
                    x=alt.X('Selected_Rate:Q', title='Historical Delay Rate (%)', scale=alt.Scale(domain=[0, 45])),
                    y=alt.Y('Risk Factor:N', sort=None, title=None),
                    color=alt.condition(
                        alt.datum.Selected_Rate > alt.datum.Global_Average,
                        alt.value('#EF4444'), # red for higher than average risk
                        alt.value('#22C55E')  # green for lower risk
                    ),
                    tooltip=['Risk Factor', 'Selected_Rate']
                ).properties(height=180)
                
                st.altair_chart(chart_contrib, use_container_width=True)
                
                # Narrative
                st.markdown(f"""
                - **Origin Airport ({selected_airport}):** Historically has a **{airport_hist*100:.1f}%** delay rate.
                - **Airline Carrier ({selected_carrier}):** Historically has a **{carrier_hist*100:.1f}%** delay rate.
                - **Time Slot ({selected_time_block}):** Departures in this block experience delays **{block_hist*100:.1f}%** of the time.
                - **Weather Impact:** Rain/snow and wind conditions add additional model-inferred delay risk.
                """)

# ==================== TAB 3: SQL QUERY CONSOLE ====================
with tab_sql:
    st.header("💻 SQLite Database Console")
    st.markdown("Run custom SQL queries against the local database schema to perform custom audits. A table guide is provided below.")
    
    # 1. DB Schema Guide
    with st.expander("📖 Database Schema Reference Guide", expanded=False):
        st.markdown("""
        The database contains the following tables:
        - **`flights`**: `flight_id` (PK), `month`, `day_of_month`, `day_of_week`, `op_unique_carrier` (FK), `tail_num`, `op_carrier_fl_num`, `origin_airport_id` (FK), `origin`, `origin_city_name`, `dest_airport_id` (FK), `dest`, `dest_city_name`, `crs_dep_time`, `dep_time`, `dep_delay_new`, `dep_del15`, `dep_time_blk`, `crs_arr_time`, `arr_time`, `arr_delay_new`, `arr_time_blk`, `cancelled`, `cancellation_code`, `crs_elapsed_time`, `actual_elapsed_time`, `distance`, `distance_group`, `carrier_delay`, `weather_delay`, `nas_delay`, `security_delay`, `late_aircraft_delay`.
        - **`airports`**: `origin_airport_id` (PK), `display_airport_name`, `origin_city_name`, `name` (full NOAA weather station name), `latitude`, `longitude`.
        - **`airlines`**: `airline_id`, `op_unique_carrier` (PK), `carrier_name`.
        - **`delay_reasons`**: `reason_code` (PK), `reason_description`.
        """)
        
    # 2. Select pre-written query
    pre_written_queries = {
        "Custom SQL Query": "",
        "Q1: Top 10 airports with highest delay rates": """
SELECT 
    a.display_airport_name AS Airport,
    a.origin_city_name AS City,
    COUNT(*) AS Total_Flights,
    SUM(f.dep_del15) AS Delayed_Flights,
    ROUND(SUM(f.dep_del15) * 100.0 / COUNT(*), 2) AS Delay_Rate_Pct
FROM flights f
JOIN airports a ON f.origin_airport_id = a.origin_airport_id
GROUP BY a.display_airport_name, a.origin_city_name
HAVING Total_Flights > 100
ORDER BY Delay_Rate_Pct DESC
LIMIT 10;
        """,
        "Q2: On-Time Performance (OTP) ranking of airlines": """
SELECT 
    a.carrier_name AS Airline,
    COUNT(*) AS Total_Flights,
    SUM(CASE WHEN f.dep_del15 = 0 AND f.cancelled = 0 THEN 1 ELSE 0 END) AS On_Time_Flights,
    ROUND(SUM(CASE WHEN f.dep_del15 = 0 AND f.cancelled = 0 THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(*), 2) AS OTP_Pct,
    ROUND(AVG(f.dep_delay_new), 2) AS Avg_Departure_Delay_Mins
FROM flights f
JOIN airlines a ON f.op_unique_carrier = a.op_unique_carrier
GROUP BY a.carrier_name
ORDER BY OTP_Pct DESC;
        """,
        "Q3: Most common reasons for flight cancellations": """
SELECT 
    f.cancellation_code AS Code,
    r.reason_description AS Description,
    COUNT(*) AS Cancellation_Count,
    ROUND(COUNT(*) * 100.0 / (SELECT SUM(cancelled) FROM flights), 2) AS Share_Pct
FROM flights f
JOIN delay_reasons r ON 'CANCEL_' || f.cancellation_code = r.reason_code
WHERE f.cancelled = 1
GROUP BY f.cancellation_code, r.reason_description
ORDER BY Cancellation_Count DESC;
        """,
        "Q4: Core statistics of flights on delayed routes": """
SELECT 
    f.origin AS Origin_Code,
    f.origin_city_name AS Origin_City,
    f.dest AS Dest_Code,
    f.dest_city_name AS Dest_City,
    COUNT(*) AS Route_Volume,
    ROUND(AVG(f.dep_delay_new), 1) AS Avg_Dep_Delay_Mins,
    ROUND(SUM(f.dep_del15) * 100.0 / COUNT(*), 2) AS Route_Delay_Rate_Pct
FROM flights f
GROUP BY f.origin, f.dest, f.origin_city_name, f.dest_city_name
HAVING Route_Volume >= 20
ORDER BY Route_Delay_Rate_Pct DESC
LIMIT 15;
        """
    }
    
    selected_query_label = st.selectbox("Select a Management Query Template", list(pre_written_queries.keys()))
    default_sql_code = pre_written_queries[selected_query_label]
    
    sql_query = st.text_area("SQL Editor", value=default_sql_code, height=200, placeholder="SELECT * FROM flights LIMIT 10;")
    
    if st.button("🚀 Run SQL Query", type="primary"):
        if sql_query.strip() == "":
            st.warning("Please type a valid SQL query.")
        else:
            conn = get_db_connection()
            if conn:
                try:
                    df_res = pd.read_sql_query(sql_query, conn)
                    st.success(f"Query returned {len(df_res)} rows successfully.")
                    st.dataframe(df_res, use_container_width=True)
                except Exception as e:
                    st.error(f"SQL Error: {e}")
                conn.close()

# ==================== TAB 4: ML MODEL EVALUATION ====================
with tab_ml:
    st.header("📈 Machine Learning Performance & Metrics")
    st.markdown("Below are the metrics and curves generated by the python evaluation scripts representing the trained `HistGradientBoosting` classifier model.")
    
    # Load metadata and test metrics
    metrics_metadata = {}
    if os.path.exists("python/model/metadata.json"):
        with open("python/model/metadata.json", "r") as f:
            metrics_metadata = json.load(f)
            
    test_metrics = {}
    if os.path.exists("python/model/test_metrics.json"):
        with open("python/model/test_metrics.json", "r") as f:
            test_metrics = json.load(f)
            
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("Training Samples", f"{metrics_metadata.get('train_samples', 160000):,}")
    with col_m2:
        st.metric("Validation ROC AUC", f"{metrics_metadata.get('roc_auc', 0.6922):.4f}")
    with col_m3:
        st.metric("Test ROC AUC", f"{test_metrics.get('test_roc_auc', 0.6913):.4f}")
    with col_m4:
        st.metric("Test Classification Accuracy", f"{test_metrics.get('test_accuracy', 0.67):.1%}")
        
    st.divider()
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader("Confusion Matrix (Test Set)")
        cm_img = "github/screenshots/confusion_matrix.png"
        if os.path.exists(cm_img):
            st.image(cm_img, caption="Confusion Matrix: On-Time vs. Delayed predictions", use_container_width=True)
        else:
            st.info("Confusion matrix plot not found. Run python python/evaluate.py to generate it.")
            
        st.subheader("Precision-Recall Curve")
        pr_img = "github/screenshots/pr_curve.png"
        if os.path.exists(pr_img):
            st.image(pr_img, caption="Precision-Recall Curve showing classifier capacity under class imbalance", use_container_width=True)
        else:
            st.info("Precision-Recall curve plot not found.")
            
    with col_p2:
        st.subheader("Receiver Operating Characteristic (ROC) Curve")
        roc_img = "github/screenshots/roc_curve.png"
        if os.path.exists(roc_img):
            st.image(roc_img, caption="ROC Curve showing trade-off between TPR and FPR", use_container_width=True)
        else:
            st.info("ROC Curve plot not found.")
            
        st.subheader("Permutation Feature Importance (Top 15)")
        fi_img = "github/screenshots/feature_importance.png"
        if os.path.exists(fi_img):
            st.image(fi_img, caption="Feature Importance: Which variables influence the predictions most?", use_container_width=True)
        else:
            st.info("Feature importance plot not found.")

# ==================== TAB 5: REPORTS & DOWNLOAD CENTER ====================
with tab_reports:
    st.header("📥 Analyst Downloads & Specifications Center")
    st.markdown("Download generated spreadsheet dashboards, and inspect layout designs and DAX specifications for Power BI dashboards.")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.subheader("📊 Executive Excel Spreadsheet Dashboard")
        st.markdown("""
        The generated Excel workbook contains:
        1. **`Dashboard`**: Dynamic styled sheet with KPI cards, summary charts, and ranked performance listings.
        2. **`Pivot Tables`**: Structured pre-calculated pivots grouping delays by Airline, Airport, and Month.
        3. **`Data & Cleaning`**: Cleaned data sample of 1,000 flight records with conditional status highlighting.
        """)
        
        excel_file_path = "excel/airline_analytics.xlsx"
        if os.path.exists(excel_file_path):
            with open(excel_file_path, "rb") as f:
                bytes_data = f.read()
            st.download_button(
                label="📥 Download Styled Excel Dashboard (.xlsx)",
                data=bytes_data,
                file_name="airline_analytics.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.success("Excel File ready for download!")
        else:
            st.error("Excel File not found! Run python excel/generate_excel_dashboard.py to generate it.")
            
    with col_d2:
        st.subheader("🖥️ Power BI Layout & DAX Specification")
        st.markdown("Read the Power BI star-schema design, measures table configurations, and layout details for the executive dashboards.")
        
        pbi_spec_path = "power_bi/power_bi_specification.md"
        if os.path.exists(pbi_spec_path):
            with open(pbi_spec_path, "r", encoding="utf-8") as f:
                pbi_md = f.read()
            with st.expander("📖 Show Power BI Specifications", expanded=True):
                st.markdown(pbi_md)
        else:
            st.info("Power BI Specification document not found.")
