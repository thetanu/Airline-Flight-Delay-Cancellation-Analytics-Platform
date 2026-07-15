<div align="center">

# ✈️ Airline Delay Prediction & Operational Analytics

### Turning flight schedules, airport weather, and carrier performance into delay predictions and operational insights

**Python** → **MySQL** → **Excel & Power BI** → **Machine Learning**

![Python](https://img.shields.io/badge/Python-Pandas%20%7C%20Sklearn-3776AB?style=for-the-badge&logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-MySQL%20%7C%20SQLite-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![Excel](https://img.shields.io/badge/Excel-openpyxl-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white) ![Status](https://img.shields.io/badge/Status-Complete-green?style=for-the-badge)

### 🚀 [**LIVE DEMO — Try the Prediction App** (click on the button)](http://localhost:8501)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://localhost:8501)

</div>

---

Every delay season, airlines and airports sit on a goldmine of logs — tail numbers, scheduled time slots, carrier codes, and historical routing patterns — but rarely turn them into an automated system that proactively flags delay risk.

This project builds an end-to-end **Airline Operations Analytics & Delay Prediction system**: clean raw flight tracking and weather datasets, model them in SQL (MySQL/SQLite), explore what actually drives delays, generate automated Excel dashboards, formulate Power BI models, and predict **departure delay probability** using machine learning.

---

## 🧾 Executive Summary

> Analyzed **4.5 million flight records** — sampling 200,000 for training a Gradient Boosted Tree model and seeding 50,000 into a relational database — alongside NOAA weather logs. Built classification models to predict **Departure Delay Status (15+ mins)** and identify network bottlenecks, achieving a **ROC-AUC of 0.69**.

---

## 🏗️ Architecture

```
📄 Raw Flight & Weather Datasets (4.5M records)
     │
     ▼
🧹 PYTHON (Pandas) — Ingestion & Cleaning
     │   (merge coordinates, join weather, extract date metrics)
     ▼
🗃️ SQL (MySQL & SQLite) — Modeling & Ingestion
     │   (normalized schema, airline/airport/weather tables, index seeds)
     ▼
📊 EXCEL & POWER BI — Reporting Layer
     │   (openpyxl script generating styled native charts & DAX specifications)
     ▼
🤖 MACHINE LEARNING — Prediction Layer
     │   (HistGradientBoosting Classifier pipeline & historical target encoding)
     ▼
🌐 STREAMLIT — Deployment
     │   (live web app: executive dashboards, prediction console, SQL terminal)
     ▼
💡 INSIGHTS LAYER — Operations Decisions
     (congested slots · weather risk mitigation · fleet allocation)
```

---

## 🧰 Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| 🧹 Data Cleaning & ETL | **Python (Pandas)** | Merging airports and weather logs, data sampling, and feature engineering |
| 🗃️ Data Modeling & SQL | **MySQL / SQLite** | Star-schema design, relational joins, table creation DDLs, and database indexing |
| 📊 Excel Dashboarding | **openpyxl (Python)** | Automating Excel creation with pivot grids, summary KPI formatting, and native charts |
| 🤖 Machine Learning | **Scikit-learn** | HistGradientBoosting classifier pipeline & target encoding configurations |
| 🌐 Deployment & UI | **Streamlit** | Serving the predictor UI, interactive executive charts, and custom SQL terminal |

---

## 📁 Dataset

- **Size:** 4,542,343 flight records, 30 columns.
- **Fields:** `flight_id`, `month`, `day_of_month`, `day_of_week`, `op_unique_carrier`, `tail_num`, `op_carrier_fl_num`, `origin_airport_id`, `origin`, `dest_airport_id`, `dest`, `crs_dep_time`, `dep_delay_new`, `dep_del15`, `cancelled`, `distance`, plus NOAA weather logs (`prcp`, `snow`, `snwd`, `tmax`, `awnd`) and target encodings (`carrier_historical`, `dep_airport_hist`, `day_historical`, `dep_block_hist`).
- **Outcome Split:** **18.91%** overall departure delay rate (delayed by 15+ minutes).

---

## 🔍 What This Project Analyzes

- **Carrier Performance:** Comparing average delay minutes and on-time performance (OTP) across 1,743 registered carriers (identifying ExpressJet `EV` as highest risk and Hawaiian `HA` as lowest).
- **Time Block Congestion:** Mapping how delay rates build up throughout the day (peaking in the **6 PM – 9 PM** block due to systemic propagation).
- **Weather Sensitivity:** Quantifying the correlation of precipitation (`PRCP`) and wind speed (`AWND`) with runway bottleneck delays.
- **Permutation Feature Importances:** Finding what features are mathematically the most critical in predicting departure delays.

---

## 📈 Machine Learning Validation & Results

The classifier predicts whether a flight will experience a departure delay of **15 minutes or more (DEP_DEL15)**. The model achieved a **ROC-AUC score of 0.69**:

### 📊 Validation Curves
| Confusion Matrix | ROC Curve |
| --- | --- |
| ![Confusion Matrix](github/screenshots/confusion_matrix.png) | ![ROC Curve](github/screenshots/roc_curve.png) |

| Precision-Recall Curve | Feature Importance |
| --- | --- |
| ![PR Curve](github/screenshots/pr_curve.png) | ![Feature Importance](github/screenshots/feature_importance.png) |

---

## 💡 Key Operational Insights

* **Late-Day Propagation:** Delay rates climb by **15%** between early morning (6 AM) and late evening (7 PM), suggesting that flight schedules have insufficient buffers.
* **Carrier Variances:** Regional airlines display significantly higher delay frequencies compared to national trunk-line carriers, indicating fleet constraints.
* **Precipitation Impact:** Every 0.5 inches of precipitation triggers an average increase of **12 minutes** in airport departure delay times.

---

## 📁 Repository Directory Layout

* 🗄️ [**`sql_database/`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/sql_database): MySQL/SQLite database schema DDLs and data ingestion script.
* 📊 [**`excel/`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/excel): Python generator code and the output spreadsheet dashboard (`airline_analytics.xlsx`).
* 🐍 [**`python/`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/python): Exploratory data analysis notebooks, model training pipelines, and validation scripts.
* 🖥️ [**`power_bi/`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/power_bi): Star-schema specs and DAX measure formulations.
* 🌐 [**`streamlit_app.py`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/streamlit_app.py): The main Streamlit web application.
