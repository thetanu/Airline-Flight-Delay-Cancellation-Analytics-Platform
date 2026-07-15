# Power BI Specification Document

This document outlines the data model, relationships, key DAX calculations, and visualization specifications for the **Airline Flight Delay & Cancellation Analytics Platform** in Power BI.

---

## 1. Data Model (Star Schema)

To ensure optimal query performance and clean report design in Power BI, the schema is structured as a **Star Schema** with `flights` acting as the central Fact table, and `airports`, `airlines`, and `delay_reasons` acting as Dimension tables.

### Tables & Relationships
1. **Fact Table:** `flights`
2. **Dimension Table (Airlines):** `airlines`
   - Relation: `flights.op_unique_carrier` (N:1) `airlines.op_unique_carrier`
   - Cross-filtering: Single (Airlines filters Flights)
3. **Dimension Table (Origin Airports):** `airports` (as Origin)
   - Relation: `flights.origin_airport_id` (N:1) `airports.origin_airport_id`
   - Cross-filtering: Single (Origin Airports filters Flights)
4. **Dimension Table (Destination Airports):** `airports` (as Destination - role-playing dimension)
   - Relation: `flights.dest_airport_id` (N:1) `airports.origin_airport_id` (Inactive relationship, activated via DAX `USERELATIONSHIP` if needed, or imported as a separate table `destination_airports`)
5. **Dimension Table (Delay Reasons):** `delay_reasons`
   - Relates conceptually to columns in `flights`. Typically handled using unpivoted delay categories in a separate bridge table, or directly mapped using DAX measures for individual delay columns in the `flights` table.
6. **Dimension Table (Calendar):** `DateTable` (Generated using DAX)
   - Relation: `flights.date` (N:1) `DateTable.Date`

---

## 2. Key DAX Calculations (Measures)

These measures should be placed in a dedicated `_Measures` table in Power BI:

### Flight Volume & Cancellation Metrics
```dax
Total Flights = COUNTROWS('flights')
```
```dax
Cancelled Flights = SUM('flights'[cancelled])
```
```dax
Cancellation Rate = DIVIDE([Cancelled Flights], [Total Flights], 0)
```

### On-Time Performance (OTP) & Delays
```dax
Delayed Flights = CALCULATE([Total Flights], 'flights'[dep_del15] = 1 && 'flights'[cancelled] = 0)
```
```dax
Delay Rate = DIVIDE([Delayed Flights], CALCULATE([Total Flights], 'flights'[cancelled] = 0), 0)
```
```dax
On-Time Flights = CALCULATE([Total Flights], 'flights'[dep_del15] = 0 && 'flights'[cancelled] = 0)
```
```dax
On-Time Performance (OTP) % = DIVIDE([On-Time Flights], CALCULATE([Total Flights], 'flights'[cancelled] = 0), 0)
```
```dax
Avg Departure Delay (Min) = AVERAGE('flights'[dep_delay_new])
```
```dax
Avg Arrival Delay (Min) = AVERAGE('flights'[arr_delay_new])
```

### Delay Breakdowns (Minutes)
```dax
Total Carrier Delay Minutes = SUM('flights'[carrier_delay])
```
```dax
Total Weather Delay Minutes = SUM('flights'[weather_delay])
```
```dax
Total NAS Delay Minutes = SUM('flights'[nas_delay])
```
```dax
Total Security Delay Minutes = SUM('flights'[security_delay])
```
```dax
Total Late Aircraft Delay Minutes = SUM('flights'[late_aircraft_delay])
```
```dax
Total Delay Minutes = [Total Carrier Delay Minutes] + [Total Weather Delay Minutes] + [Total NAS Delay Minutes] + [Total Security Delay Minutes] + [Total Late Aircraft Delay Minutes]
```

### Delay Reason % of Total Delay Minutes
```dax
Carrier Delay % = DIVIDE([Total Carrier Delay Minutes], [Total Delay Minutes], 0)
```
```dax
Weather Delay % = DIVIDE([Total Weather Delay Minutes], [Total Delay Minutes], 0)
```
```dax
NAS Delay % = DIVIDE([Total NAS Delay Minutes], [Total Delay Minutes], 0)
```
```dax
Security Delay % = DIVIDE([Total Security Delay Minutes], [Total Delay Minutes], 0)
```
```dax
Late Aircraft Delay % = DIVIDE([Total Late Aircraft Delay Minutes], [Total Delay Minutes], 0)
```

---

## 3. Dashboard Page Layouts

### Page 1: Executive Dashboard (Stakeholder Overview)
* **Goal:** High-level operational summary for executives to monitor airline reliability and delay costs.
* **KPI Cards (Top Row):**
  - `Total Flights` (Volume)
  - `On-Time Performance (OTP) %` (Goal: > 80%)
  - `Average Departure Delay (min)`
  - `Cancellation Rate %` (Goal: < 2%)
* **Visualizations:**
  - **Clustered Column Chart:** OTP % vs. Delay Rate % by Month (Monthly Performance).
  - **Bar Chart:** OTP % by Airline (Airlines ranked by reliability).
  - **Donut Chart:** Total Delay Minutes by Delay Category (Carrier vs. Weather vs. NAS, etc.).
  - **Map Visual:** Origin Airports sized by `Total Flights` and colored by `OTP %` (Geographic bottlenecks).

### Page 2: Airport Dashboard (Bottlenecks & Efficiency)
* **Goal:** Identify airports that experience the most congestion and weather-related operational bottlenecks.
* **KPI Cards:**
  - `Average Departure Delay (min)`
  - `Highest Delay Airport` (Text measure)
  - `Total Delayed Departures`
* **Visualizations:**
  - **Table (Top Bottlenecks):** Airport Name | City | Total Departures | Delay Rate % | Avg Delay (min) | Weather Delay (min).
  - **Scatter Plot:** Average Delay (Y-axis) vs. Flight Volume (X-axis) (To isolate high-volume congested hubs from low-volume highly-delayed airports).
  - **Tornado Chart:** Inbound vs. Outbound Delays (comparing origin and destination performance).

### Page 3: Airline Dashboard (Competitive Performance)
* **Goal:** Compare airlines to find the best on-time performances and fleet age correlations.
* **KPI Cards:**
  - `Top Performing Airline` (Best OTP %)
  - `Worst Performing Airline` (Worst OTP %)
  - `Average Fleet Age` (From plane database)
* **Visualizations:**
  - **Matrix Visual:** Airline | Total Flights | OTP % | Avg Departure Delay | Carrier Delay (min) | Late Aircraft Delay (min).
  - **Line Chart:** OTP % trend of top 5 airlines across days of the week.
  - **Scatter Chart:** Average Delay (Y-axis) vs. Average Plane Age (X-axis) (Correlation between aircraft age and maintenance delays).

### Page 4: Delay Analysis Dashboard (Root-Cause Investigation)
* **Goal:** Drill down into the specific factors contributing to flight delays.
* **KPI Cards:**
  - `Primary Delay Contributor` (Dynamic text card)
  - `Average Carrier Delay (min)`
  - `Average Weather Delay (min)`
* **Visualizations:**
  - **100% Stacked Bar Chart:** Delay Reasons % Breakdown by Airline (Which airlines struggle with maintenance vs. scheduling).
  - **Line Chart:** Weather Delay Minutes vs. Daily Precipitation (PRCP) / Snowfall (SNOW) (Weather correlation analysis).
  - **Heatmap Grid:** Day of Week (Rows) vs. Departure Time Block (Columns) colored by Delay Rate (Peak bottleneck times during the week).

### Page 5: Cancellation Analysis Dashboard (Operational Failure)
* **Goal:** Analyze why flights are cancelled and identify patterns.
* **KPI Cards:**
  - `Cancellation Rate`
  - `Total Cancelled Flights`
  - `Most Common Cancellation Code` (Carrier vs. Weather vs. NAS)
* **Visualizations:**
  - **Pie Chart:** Cancellation Volume by Code (A = Carrier, B = Weather, C = NAS, D = Security).
  - **Area Chart:** Daily Cancellation Trend overlaying daily wind speeds (`AWND`) or precipitation (`PRCP`) (To prove weather impact).
  - **Bar Chart:** Cancellation Rate by Airline (Which carriers cancel the most flights).

---

## 4. Theme & Design Aesthetics

* **Color Palette (Modern Steel & Corporate Trust):**
  - Primary Dark Blue (Headers/KPI numbers): `#1F4E78`
  - Secondary Light Blue (Selection/Accents): `#5B9BD5`
  - Highlight Accent (Zebra rows/Card fills): `#D9E1F2`
  - Warning Red (Delayed/Cancelled states): `#C00000`
  - Neutral Gray (Secondary text/Gridlines): `#7F7F7F`
* **Typography:** Segoe UI (Standard Power BI font for maximum compatibility and clean look).
* **Interactivity:**
  - Tooltips enabled on all charts to show exact delay breakups.
  - Cross-filtering enabled between map, list, and charts.
  - "Drill-through" enabled from Executive Dashboard to Airport Dashboard.
