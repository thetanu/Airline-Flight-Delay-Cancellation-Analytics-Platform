# Presentation: Flight Delay & Cancellation Analytics
**Stakeholder Slide Deck Outline**  
*Audience: Executive Leadership, Heads of Operations, Route Planners*

---

## Slide 1: Title Slide
* **Title:** Optimizing Airline Operations through Predictive Data Analytics
* **Subtitle:** Understanding, Forecasting, and Mitigating Flight Delays & Cancellations
* **Speaker:** Operations Data Analyst
* **Visual:** Premium graphic of flight network.

---

## Slide 2: The Business Challenge
* **The Cost of Delays:**
  - Cascading crew hours & overtime costs.
  - Fuel burn during ground holding and terminal holding.
  - Brand damage and passenger churn.
* **Key Questions for Today:**
  - Which airports and airlines represent our biggest operational risks?
  - Can we predict flight delays *before* they disrupt the schedule?
  - What actionable strategies can reduce cancellations?

---

## Slide 3: SQL Data Infrastructure & Pipeline
* **Star-Schema Database Setup:**
  - **Fact Table:** `flights` (seeding records, departures, arrivals, cancellations).
  - **Dimension Tables:** `airports` (geographics, NOAA weather stations), `airlines` (carrier registry), `delay_reasons`.
* **ETL Pipeline:**
  - Built-in SQLAlchemy ingestion script loading and joining raw flight logs and weather CSVs.
  - SQLite database out-of-the-box, easily scaled to MySQL Workbench for server storage.

---

## Slide 4: Airport & Airline Insights
* **Top Airport Bottlenecks:**
  - Chicago O'Hare (ORD) leads with a **24.1%** delay rate.
  - Newark (EWR) and Denver (DEN) closely follow due to congestion and snow.
* **Airline On-Time Rankings (OTP):**
  - **Best Performers:** Hawaiian (89.2%), Southwest (83.5%), Delta (82.8%).
  - **Struggling Carriers:** JetBlue (72.1%) and regional feeders.

---

## Slide 5: Root Causes of Delays
* **Why do flights fail to depart on time?**
  - **Late Aircraft Cascades (Primary):** Downstream segments inherit delays from early-morning flights.
  - **Airspace Density (NAS):** High volume of concurrent departures in afternoon time slots.
  - **Weather:** Rain, snow, and crosswinds limit runway capacity.

---

## Slide 6: Pre-Departure ML Predictor
* **The Solution:** A machine learning model forecasting delays *before* passenger boarding.
* **Model Specifics:**
  - Trained on 200,000 operations sample.
  - Uses `HistGradientBoostingClassifier` to natively handle tabular missingness.
  - **ROC AUC:** 0.6913, providing a strong lift over random guessing.
* **Top Predictors:** Historical airport delay rates, scheduled time block, concurrent departures count, precipitation.

---

## Slide 7: Interactive Analytics Platform Demonstration
* **Features of the Streamlit App:**
  - **Executive Dashboard:** Live Altair interactive charts.
  - **Delay Predictor:** Real-time delay risk assessment widget.
  - **Database SQL Console:** Console to execute audit queries directly.
  - **Report Downloads:** Cleaned Excel sheets and Power BI templates.

---

## Slide 8: Strategic Operations Recommendations
* **1. Route-Level Consolidation:** Consolidate congested routes (e.g. ORD-LGA) to reduce flight frequency while holding capacity using larger aircraft.
* **2. Reschedule Multi-Segment Feeder Loops:** Allocate 45-minute buffers for aircraft scheduled for more than 3 segments per day.
* **3. Dynamic Customer Re-accommodation:** Integrate ML delay risk scores into reservations, offering early voluntary re-routing to bypass winter storm centers.
* **4. Dynamic Crew Allocation:** Place fast-turnaround crews on high-risk airport departures.
