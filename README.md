# ✈️ Airline Flight Delay & Cancellation Analytics Platform

Welcome to the **Airline Flight Delay & Cancellation Analytics Platform**. This platform is a complete, end-to-end data analytics and predictive modeling system designed to help airlines analyze delay factors, monitor operational reliability, identify airport bottlenecks, and predict flight delays before departure.

**Developer & Author:** Tanu Tyagi  

---

> [!WARNING]
> **No Real-Time Analysis:** This platform does not perform live, real-time streaming analysis. It processes and visualizes batch historical data (SQLite/MySQL) to generate predictions and analytical dashboards.

---

## 🚀 Key Features

* **📊 Executive KPI Dashboard:** Interactive visual analytics built with Streamlit and Altair displaying on-time performance (OTP), delay metrics, and cancellation rates.
* **🔮 Delay Predictor:** Custom-trained Machine Learning model (Gradient Boosted Trees) that estimates the probability of pre-departure flight delays based on weather, time slot, carrier, and airport.
* **💻 Interactive SQL Console:** A built-in SQLite/MySQL query console with preloaded operational templates for custom data exploration.
* **📊 Excel Visual Dashboard:** Automatically generated, styled Excel workbook containing formatted raw logs, pre-calculated pivot tables, and native Excel charts.
* **🖥️ Power BI Layout Spec:** Complete star-schema specifications and DAX measures ready to build clean, optimized reports.

---

## 📂 Directory Layout

* 🗄️ [**`sql_database/`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/sql_database): Schema design (`schema.sql`) and database ETL ingestion scripts.
* 📊 [**`excel/`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/excel): Python generator script (`generate_excel_dashboard.py`) and the output spreadsheet.
* 🐍 [**`python/`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/python): Explanatory analysis notebooks, ML training/evaluation pipelines.
* 🖥️ [**`power_bi/`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/power_bi): Star-schema relationships and DAX specifications.
* 🌐 [**`streamlit_app.py`**](file:///c:/Users/ntanu/OneDrive/Desktop/Airline%20Flight%20Delay%20&%20Cancellation%20Analytics%20Platform/streamlit_app.py): The entry point for the interactive web frontend.

---

## 🛠️ Quick Start Guide

Ensure you have Python 3.8+ installed. You can install all dependencies by running:

```bash
pip install pandas numpy scikit-learn openpyxl sqlalchemy streamlit altair matplotlib seaborn python-dotenv pymysql cryptography
```

### 1. Ingest Data (SQLite / MySQL)
Seeding the database creates a local SQLite database by default, or connects to MySQL if configured in `.env`.
```bash
python sql_database/import_data.py
```

### 2. Generate the Excel Visual Dashboard
```bash
python excel/generate_excel_dashboard.py
```

### 3. Run the ML Pipeline (Train & Evaluate)
```bash
python python/train.py
python python/generate_historical_rates.py
python python/evaluate.py
```

### 4. Launch the Streamlit Frontend App
```bash
python -m streamlit run streamlit_app.py
```
Open the local URL `http://localhost:8501` in your browser.

---

## ☁️ Streamlit Deployment Guide

To deploy this interactive Streamlit app to the web for free using **Streamlit Community Cloud**:

1. **Push your code to GitHub** (follow the steps below).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **"Create App"** or **"New App"**.
4. Select your repository, branch (e.g. `main`), and set the Main file path to **`streamlit_app.py`**.
5. **Database Configuration:**
   * By default, the app will look for the local SQLite database. Ensure `sql_database/airline_analytics.db` is created.
   * If connecting to an external MySQL server, set your `DATABASE_URL` in the Streamlit **Secrets** configuration menu:
     ```toml
     DATABASE_URL = "mysql+pymysql://<user>:<password>@<host>:3306/<database_name>"
     ```
6. Click **Deploy!** Your app will be live on a public URL.

---

## 📈 Git & GitHub Ingestion

To push this repository to your GitHub account:

1. Initialize Git in the project root:
   ```bash
   git init
   ```
2. Stage all files (sensitive files like `.env` and large DBs are ignored by `.gitignore`):
   ```bash
   git add .
   ```
3. Commit the code:
   ```bash
   git commit -m "Initial commit - Airline Delay Analytics Platform by Tanu Tyagi"
   ```
4. Link your remote GitHub repository and push:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```
