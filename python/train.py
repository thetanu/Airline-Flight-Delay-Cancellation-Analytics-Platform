import os
import pandas as pd
import numpy as np
import time
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

# Import preprocessor and feature configurations
from feature_engineering import FlightDataPreprocessor, CATEGORICAL_COLS, NUMERICAL_COLS, TARGET_COL

train_path = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\archive (5)\train.csv'
model_dir = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\python\model'

os.makedirs(model_dir, exist_ok=True)

def train_model():
    print("Loading training dataset...")
    start_time = time.time()
    
    # Read the full dataset (it fits in memory, but we use a sample to speed up training)
    df = pd.read_csv(train_path)
    print(f"Loaded {len(df)} rows in {time.time() - start_time:.2f} seconds.")
    
    # Perform stratified sampling to extract 200,000 rows
    print("Sampling 200,000 records for model training...")
    sample_size = 200000
    df_sample = df.sample(n=sample_size, random_state=42, weights=None)
    
    # Check target class distribution
    dist = df_sample[TARGET_COL].value_counts(normalize=True)
    print(f"Sample target class distribution: \n{dist}")
    
    X = df_sample.drop(columns=[TARGET_COL])
    y = df_sample[TARGET_COL]
    
    # Split into train/validation sets (80/20)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    print(f"Training set size: {X_train.shape}, Validation set size: {X_val.shape}")
    
    # Initialize Preprocessor
    preprocessor = FlightDataPreprocessor()
    
    # Initialize HistGradientBoostingClassifier
    # We specify which feature indices are categorical
    # Our preprocessed features will have categoricals in the first 4 columns (indices 0, 1, 2, 3)
    categorical_features_mask = [True, True, True, True] + [False] * len(NUMERICAL_COLS)
    
    model = HistGradientBoostingClassifier(
        max_iter=150,
        learning_rate=0.08,
        max_depth=6,
        min_samples_leaf=20,
        categorical_features=categorical_features_mask,
        random_state=42,
        class_weight='balanced'  # Compensate for class imbalance
    )
    
    # Build pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])
    
    print("Fitting preprocessing and machine learning pipeline...")
    fit_start = time.time()
    pipeline.fit(X_train, y_train)
    print(f"Model training complete in {time.time() - fit_start:.2f} seconds.")
    
    # Evaluate on validation set
    y_pred = pipeline.predict(X_val)
    y_prob = pipeline.predict_proba(X_val)[:, 1]
    
    roc_auc = roc_auc_score(y_val, y_prob)
    print("\nValidation Set Metrics:")
    print(f"ROC AUC Score: {roc_auc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_val, y_pred))
    
    # Save validation metrics
    metrics = {
        "train_samples": len(X_train),
        "val_samples": len(X_val),
        "roc_auc": float(roc_auc),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save the pipeline
    model_path = os.path.join(model_dir, "flight_delay_model.joblib")
    joblib.dump(pipeline, model_path)
    print(f"Pipeline successfully saved to: {model_path}")
    
    # Save unique categories for Streamlit UI menus
    categories_path = os.path.join(model_dir, "categories.json")
    with open(categories_path, "w") as f:
        json.dump(preprocessor.categories_, f, indent=4)
    print(f"Unique categories saved to: {categories_path}")
    
    # Save training metadata
    metadata_path = os.path.join(model_dir, "metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Metadata saved to: {metadata_path}")

if __name__ == "__main__":
    train_model()
