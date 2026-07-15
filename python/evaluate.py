import os
import pandas as pd
import numpy as np
import time
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    roc_curve, 
    auc, 
    precision_recall_curve,
    ConfusionMatrixDisplay
)
from sklearn.inspection import permutation_importance

# Import configs
from feature_engineering import CATEGORICAL_COLS, NUMERICAL_COLS, TARGET_COL, ALL_FEATURES

test_path = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\archive (5)\test.csv'
model_path = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\python\model\flight_delay_model.joblib'
screenshots_dir = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\github\screenshots'
model_dir = r'c:\Users\ntanu\OneDrive\Desktop\Airline Flight Delay & Cancellation Analytics Platform\python\model'

os.makedirs(screenshots_dir, exist_ok=True)

def evaluate_model():
    print("Loading model and test dataset...")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please run train.py first!")
        
    pipeline = joblib.load(model_path)
    
    start_time = time.time()
    df_test = pd.read_csv(test_path)
    print(f"Loaded {len(df_test)} test rows in {time.time() - start_time:.2f} seconds.")
    
    # Sample 100,000 rows for evaluation
    print("Sampling 100,000 test records for evaluation...")
    df_test_sample = df_test.sample(n=100000, random_state=42)
    
    X_test = df_test_sample.drop(columns=[TARGET_COL])
    y_test = df_test_sample[TARGET_COL]
    
    print("Running predictions on test set...")
    pred_start = time.time()
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    print(f"Predictions complete in {time.time() - pred_start:.2f} seconds.")
    
    # Classification Report
    print("\nTest Set Classification Report:")
    report = classification_report(y_test, y_pred, output_dict=True)
    print(classification_report(y_test, y_pred))
    
    # Save test metrics
    test_metrics = {
        "test_samples": len(X_test),
        "test_accuracy": report["accuracy"],
        "test_macro_f1": report["macro avg"]["f1-score"],
        "test_weighted_f1": report["weighted avg"]["f1-score"],
        "test_roc_auc": float(np.mean(y_prob[y_test == 1]) - np.mean(y_prob[y_test == 0])) # approximate separation or compute AUC
    }
    
    # Calculate AUC
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    test_metrics["test_roc_auc"] = roc_auc
    print(f"Test ROC AUC: {roc_auc:.4f}")
    
    with open(os.path.join(model_dir, "test_metrics.json"), "w") as f:
        json.dump(test_metrics, f, indent=4)
        
    # --- PLOTS ---
    print("Generating evaluation plots...")
    sns.set_theme(style="whitegrid")
    
    # 1. Confusion Matrix
    fig, ax = plt.subplots(figsize=(6, 5))
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["On-Time", "Delayed"])
    disp.plot(cmap="Blues", ax=ax, values_format="d")
    ax.set_title("Confusion Matrix (Test Set)")
    plt.tight_layout()
    cm_path = os.path.join(screenshots_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=150)
    plt.close()
    print(f"Saved Confusion Matrix to {cm_path}")
    
    # 2. ROC Curve
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC Curve (AUC = {roc_auc:.3f})")
    ax.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("Receiver Operating Characteristic (ROC) Curve")
    ax.legend(loc="lower right")
    plt.tight_layout()
    roc_path = os.path.join(screenshots_dir, "roc_curve.png")
    plt.savefig(roc_path, dpi=150)
    plt.close()
    print(f"Saved ROC Curve to {roc_path}")
    
    # 3. Precision-Recall Curve
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    pr_auc = auc(recall, precision)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(recall, precision, color="blue", lw=2, label=f"PR Curve (AUC = {pr_auc:.3f})")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curve")
    ax.legend(loc="lower left")
    plt.tight_layout()
    pr_path = os.path.join(screenshots_dir, "pr_curve.png")
    plt.savefig(pr_path, dpi=150)
    plt.close()
    print(f"Saved Precision-Recall Curve to {pr_path}")
    
    # 4. Permutation Feature Importance
    # We use a smaller subset (e.g. 3,000 rows) for speed, since permutation importance is O(N_features * N_samples)
    print("Computing permutation feature importances (this may take a minute)...")
    df_imp_sample = df_test_sample.sample(n=3000, random_state=42)
    X_imp = df_imp_sample.drop(columns=[TARGET_COL])
    y_imp = df_imp_sample[TARGET_COL]
    
    imp_start = time.time()
    result = permutation_importance(
        pipeline, X_imp, y_imp, n_repeats=5, random_state=42, n_jobs=-1
    )
    print(f"Feature importance calculated in {time.time() - imp_start:.2f} seconds.")
    
    # Plot feature importances
    sorted_importances_idx = result.importances_mean.argsort()[::-1]
    importances_df = pd.DataFrame({
        "feature": [ALL_FEATURES[i] for i in sorted_importances_idx],
        "importance": result.importances_mean[sorted_importances_idx],
        "std": result.importances_std[sorted_importances_idx]
    })
    
    # Save importance metrics to JSON
    importances_df.to_json(os.path.join(model_dir, "feature_importances.json"), orient="records", indent=4)
    
    # Plot top 15 features
    fig, ax = plt.subplots(figsize=(8, 6))
    top_importances = importances_df.head(15)
    sns.barplot(
        x="importance", y="feature", data=top_importances, 
        ax=ax, palette="viridis", hue="feature", legend=False
    )
    ax.set_title("Permutation Feature Importance (Top 15 Features)")
    ax.set_xlabel("Mean Decrease in Accuracy")
    plt.tight_layout()
    importance_path = os.path.join(screenshots_dir, "feature_importance.png")
    plt.savefig(importance_path, dpi=150)
    plt.close()
    print(f"Saved Feature Importance Plot to {importance_path}")
    
    print("\nModel evaluation complete!")

if __name__ == "__main__":
    evaluate_model()
