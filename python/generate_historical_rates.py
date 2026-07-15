import pandas as pd
import json
import os

train_path = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\archive (5)\train.csv'
model_dir = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\python\model'

def generate_rates():
    print("Loading training data for historical rates generation...")
    df = pd.read_csv(train_path, usecols=[
        'CARRIER_NAME', 'DEPARTING_AIRPORT', 'DAY_OF_WEEK', 'DEP_TIME_BLK', 'DEP_DEL15'
    ])
    
    # Global average delay rate fallback
    global_mean = float(df['DEP_DEL15'].mean())
    print(f"Global historical delay rate: {global_mean:.4f}")
    
    # Carrier rates
    carrier_rates = df.groupby('CARRIER_NAME')['DEP_DEL15'].mean().to_dict()
    # Airport rates
    airport_rates = df.groupby('DEPARTING_AIRPORT')['DEP_DEL15'].mean().to_dict()
    # Day rates
    day_rates = df.groupby('DAY_OF_WEEK')['DEP_DEL15'].mean().to_dict()
    # Time block rates
    block_rates = df.groupby('DEP_TIME_BLK')['DEP_DEL15'].mean().to_dict()
    
    rates = {
        "global_mean": global_mean,
        "carrier_rates": {str(k): float(v) for k, v in carrier_rates.items()},
        "airport_rates": {str(k): float(v) for k, v in airport_rates.items()},
        "day_rates": {str(k): float(v) for k, v in day_rates.items()},
        "block_rates": {str(k): float(v) for k, v in block_rates.items()}
    }
    
    os.makedirs(model_dir, exist_ok=True)
    rates_path = os.path.join(model_dir, "historical_rates.json")
    with open(rates_path, "w") as f:
        json.dump(rates, f, indent=4)
        
    print(f"Historical rates successfully saved to: {rates_path}")

if __name__ == "__main__":
    generate_rates()
