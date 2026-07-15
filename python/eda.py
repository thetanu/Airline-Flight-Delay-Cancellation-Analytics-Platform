import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

train_path = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\archive (5)\train.csv'
eda_plots_dir = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\github\screenshots'

os.makedirs(eda_plots_dir, exist_ok=True)

def run_eda():
    print("Loading sample data for Exploratory Data Analysis...")
    # Load 100k rows sample for fast plotting
    df = pd.read_csv(train_path, nrows=100000)
    
    print(f"Data shape: {df.shape}")
    print("\nColumns and non-null counts:")
    print(df.info())
    
    # Configure styling
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    
    # 1. Plot Target Variable Distribution
    print("Generating class distribution plot...")
    plt.figure(figsize=(6, 4))
    sns.countplot(x='DEP_DEL15', data=df, hue='DEP_DEL15', palette='Blues', legend=False)
    plt.title("Distribution of Departure Delays (>15 mins)")
    plt.xlabel("Is Delayed (0 = On-Time, 1 = Delayed)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(eda_plots_dir, "eda_target_distribution.png"), dpi=150)
    plt.close()
    
    # 2. Plot Delay Rate by Airline
    print("Generating delay rate by airline plot...")
    plt.figure(figsize=(10, 6))
    airline_delays = df.groupby('CARRIER_NAME')['DEP_DEL15'].mean().reset_index().sort_values(by='DEP_DEL15', ascending=False)
    sns.barplot(x='DEP_DEL15', y='CARRIER_NAME', data=airline_delays, hue='CARRIER_NAME', palette='viridis', legend=False)
    plt.title("Historical Delay Rate by Airline Carrier")
    plt.xlabel("Delay Rate (%)")
    plt.ylabel("Airline")
    plt.tight_layout()
    plt.savefig(os.path.join(eda_plots_dir, "eda_airline_delays.png"), dpi=150)
    plt.close()
    
    # 3. Plot Delay Rate by Departure Time Block
    print("Generating delay rate by time block plot...")
    plt.figure(figsize=(10, 5))
    block_delays = df.groupby('DEP_TIME_BLK')['DEP_DEL15'].mean().reset_index().sort_values(by='DEP_TIME_BLK')
    sns.lineplot(x='DEP_TIME_BLK', y='DEP_DEL15', data=block_delays, marker='o', color='#1F4E78', linewidth=2)
    plt.xticks(rotation=45)
    plt.title("Delay Probability by Scheduled Departure Time Slot")
    plt.xlabel("Departure Time Block")
    plt.ylabel("Delay Rate (%)")
    plt.tight_layout()
    plt.savefig(os.path.join(eda_plots_dir, "eda_time_block_delays.png"), dpi=150)
    plt.close()
    
    # 4. Correlation of Weather Features with Delay Status
    print("Generating weather features correlation heatmap...")
    weather_cols = ['DEP_DEL15', 'PRCP', 'SNOW', 'SNWD', 'TMAX', 'AWND', 'PLANE_AGE']
    corr_matrix = df[weather_cols].corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.3f', linewidths=0.5, vmin=-1.0, vmax=1.0)
    plt.title("Correlation Matrix: Delays, Weather, and Aircraft Age")
    plt.tight_layout()
    plt.savefig(os.path.join(eda_plots_dir, "eda_weather_correlation.png"), dpi=150)
    plt.close()
    
    print("EDA completed successfully and charts exported!")

if __name__ == "__main__":
    run_eda()
