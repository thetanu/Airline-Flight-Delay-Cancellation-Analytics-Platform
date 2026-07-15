# ✈️ Airline Flight Delay & Cancellation Analytics Platform

An end-to-end data analytics and predictive modeling platform designed to help airlines monitor operational reliability, identify airport bottlenecks, analyze delay factors, and predict flight delays before departure.

---

## 📂 Project Structure

```
├── sql_database/
│      ├── schema.sql                 # MySQL-compatible database DDL
│      ├── import_data.py             # Python ETL & database ingestion script
│      └── airline_analytics.db       # SQLite local database (generated)
│
├── excel/
│      ├── generate_excel_dashboard.py# Automated Excel workbook generator
│      └── airline_analytics.xlsx     # Styled spreadsheet dashboard (generated)
│
├── python/
│      ├── feature_engineering.py     # Preprocessing & categorical encoding module
│      ├── train.py                   # Machine learning model training script
│      ├── evaluate.py                # Model evaluation and plot generator
│      ├── generate_historical_rates.py# Script computing delay rate target encodings
│      └── model/                     # Serialized models & metadata configurations
│
├── power_bi/
│      └── power_bi_specification.md  # Star-schema relationships & DAX specifications
│
├── github/
│      ├── README.md                  # Project overview and installation guide (this file)
│      ├── report.md                  # Comprehensive analyst operations report
│      ├── presentation.md            # Stakeholder slide deck outline
│      └── screenshots/               # Model curves and metrics plots (generated)
│
└── streamlit_app.py                  # Interactive Streamlit application (app entry point)
```

---

## 🛠️ Installation & Setup

Ensure you have Python 3.8+ installed. You can install all dependencies by running:

```bash
pip install pandas numpy scikit-learn openpyxl sqlalchemy streamlit altair matplotlib seaborn python-dotenv
```

### 1. Ingestion of Database
By default, the pipeline creates a zero-setup **SQLite** database `sql_database/airline_analytics.db` populated with a sample of **50,000 operations** from the raw data.
To run the database ingestion pipeline:
```bash
python sql_database/import_data.py
```

### 2. Integration with MySQL Workbench (Optional)
To store data in a centralized **MySQL** database instead of SQLite:
1. Make sure you have a running MySQL server.
2. Install the MySQL python driver:
   ```bash
   pip install pymysql cryptography
   ```
3. Copy `.env.example` to `.env` and uncomment the MySQL configuration line:
   ```env
   DATABASE_URL=mysql+pymysql://<user>:<password>@localhost:3306/<database_name>
   ```
4. Re-run `python sql_database/import_data.py`. The tables will be created and populated directly inside your MySQL database, allowing you to connect and run queries inside **MySQL Workbench**.

### 3. Generate the Excel Dashboard
To generate a fully styled, multi-sheet Excel dashboard `excel/airline_analytics.xlsx` populated with operational pivots and native bar/line charts:
```bash
python excel/generate_excel_dashboard.py
```

### 4. Train the ML Predictor
To fit the pre-departure delay model on **200,000 training records** and generate evaluation plots in the `github/screenshots/` directory:
```bash
python python/train.py
python python/generate_historical_rates.py
python python/evaluate.py
```

### 5. Launch the Streamlit Frontend App
To spin up the interactive user interface locally:
```bash
streamlit run streamlit_app.py
```

---

## 🖥️ Streamlit App Features

1. **📊 Executive KPI Dashboard:** Dynamic dashboard presenting total flights, average delays, OTP, and cancellation rates, supported by interactive visual metrics in Altair.
2. **🔮 Interactive Delay Predictor:** A web form allowing users to select airline, origin/previous airports, departure times, and weather conditions to forecast flight delay probability with risk factor breakups.
3. **💻 SQL Console:** Run custom queries directly against the live database or choose from pre-written management query templates to analyze operational data.
4. **📈 ML Model Evaluation:** Displays metrics, confusion matrices, ROC/PR curves, and feature importances showing model efficacy.
5. **📥 Download Center:** Direct button to download the styled Excel dashboard and view Power BI specifications.
