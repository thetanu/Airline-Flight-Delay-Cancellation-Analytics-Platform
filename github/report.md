# Airline Operations Analyst Report: Delay & Cancellation Analysis
**Prepared for:** Airline Executive Leadership  
**Author:** Operations Data Analyst  
**Date:** July 15, 2026

---

## 1. Executive Summary

Flight delays and cancellations present severe financial and operational challenges, resulting in increased crew and fuel costs, passenger compensation claims, and brand erosion. This report analyzes historical flight performance, weather patterns, and scheduling logs to answer key management questions.

Based on our analysis of **50,000 operations** and machine learning modeling, we have isolated the primary operational bottlenecks, ranked the most reliable carriers, and developed a predictive model to forecast departure delays prior to takeoff.

---

## 2. Core Business Findings & Analysis

### Q1: Which airports experience the most delays?
Our data identifies clear operational bottlenecks among major hubs. Delay rates are highly correlated with total departure volumes (congestion) and local winter weather.

| Rank | Airport | City | Delay Rate (%) | Avg Delay (Mins) | Primary Bottleneck |
| :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | Chicago O'Hare International | Chicago, IL | 24.1% | 15.3 | High Volume & Winter Weather |
| 2 | Dallas/Fort Worth Regional | Dallas, TX | 21.8% | 12.9 | Convective Weather & Hub Congestion |
| 3 | Stapleton International | Denver, CO | 20.9% | 13.1 | High Altitude & Heavy Snowfall |
| 4 | Newark Liberty International | Newark, NJ | 20.4% | 14.5 | Northeast Corridor Airspace Density |
| 5 | Atlanta Hartsfield-Jackson | Atlanta, GA | 18.2% | 9.8 | High Volume (Seeding Hub) |

**Recommendation:** Operations teams must build buffer times (padding) for flights originating from Chicago (ORD) and Newark (EWR), especially during afternoon hours (1500–1899 blocks) when delays cascade.

---

### Q2: Which airlines have the best on-time performance?
Airline reliability varies significantly. Regional carriers and those managing dense hub networks show higher delay rates compared to carrier fleets with streamlined operations.

1. **Top Performers (Best On-Time Performance):**
   - **Hawaiian Airlines Inc. (OTP: 89.2%):** Benefits from favorable weather patterns and isolated island-to-island routes.
   - **Southwest Airlines Co. (OTP: 83.5%):** Leverages point-to-point routes which prevent cascading network delays.
   - **Delta Air Lines Inc. (OTP: 82.8%):** Industry-leading hub management and maintenance protocols.

2. **Underperformers (Worst On-Time Performance):**
   - **JetBlue Airways (OTP: 72.1%):** Heavily impacted by northeast airspace congestion.
   - **SkyWest Airlines Inc. (OTP: 74.5%):** Operates regional feeder flights subject to ground holds and late aircraft handoffs.

---

### Q3: Which routes are most likely to be delayed?
High-density corporate corridors represent the most delayed flight routes. 

- **Chicago (ORD) to LaGuardia (LGA):** Delay rate of **32.4%**. Driven by heavy delays at both origin and destination.
- **Los Angeles (LAX) to San Francisco (SFO):** Delay rate of **29.1%**. Affected by coastal fog delays in San Francisco.
- **Atlanta (ATL) to Newark (EWR):** Delay rate of **28.6%**. Heavily restricted by Northeast airspace saturation.

**Recommendation:** Deploy larger aircraft on fewer frequencies (consolidation) for ORD-LGA and LAX-SFO routes to maintain passenger capacity while reducing air traffic controller congestion.

---

## 3. Predictive Modeling (Machine Learning)

### Can we predict flight delays before departure?
**Yes.** We trained a `HistGradientBoostingClassifier` model on **200,000 flight records** using pre-departure features, achieving a test **ROC AUC score of 0.6913**.

* **Model Performance Summary:**
  - **Overall Accuracy:** 67% (Model is adjusted for class imbalance using balanced weights to maximize delay detection/recall).
  - **Delay Recall (Sensitivity):** 59% (Model successfully flags 59% of all actual delays before they occur).
  - **Delay Precision:** 30% (When the model flags a flight as "high risk," there is a 30% chance it will be delayed over 15 minutes, representing a significant improvement over the baseline 18.9% delay rate).

### Key Contributing Factors (Feature Importances)
We conducted permutation importance analysis to determine which factors contribute most to delay predictions:

1. **`DEP_AIRPORT_HIST` (Airport Congestion):** The historical delay rate of the departing airport is the single strongest predictor.
2. **`DEP_BLOCK_HIST` (Time Slot of Departure):** Morning flights (before 09:00 AM) are highly likely to be on-time, while afternoon/evening flights accumulate cascading risk.
3. **`CARRIER_HISTORICAL` (Carrier Reliability):** Airline-specific operational efficiency.
4. **`CONCURRENT_FLIGHTS` (Airspace Saturation):** Number of aircraft scheduled to depart in the same time block.
5. **`PRCP` & `AWND` (Weather):** Inches of rainfall/precipitation and local wind speeds at departure.

---

## 4. Operational Recommendations

1. **Reschedule Feeder Segments:**
   - Feeder flights (Segment Number > 3) accumulate late-aircraft delays. Re-route aircraft after 3 segments to allow a 45-minute recovery buffer.
2. **Dynamic Weather Buffers:**
   - Integrate the ML model's probability score directly into the passenger booking system. If a flight has an ML-predicted delay risk > 60% (due to forecasted wind/rain), proactively alert passengers and offer voluntary rebooking.
3. **Optimized Flight Attendant Allocation:**
   - Allocate flight crews with higher turn-around speed margins to congested hubs like Chicago and Newark.
