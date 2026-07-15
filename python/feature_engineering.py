import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OrdinalEncoder

# Lists of columns
CATEGORICAL_COLS = ['DEP_TIME_BLK', 'CARRIER_NAME', 'DEPARTING_AIRPORT', 'PREVIOUS_AIRPORT']

NUMERICAL_COLS = [
    'MONTH', 'DAY_OF_WEEK', 'DISTANCE_GROUP', 'SEGMENT_NUMBER', 
    'CONCURRENT_FLIGHTS', 'NUMBER_OF_SEATS', 'AIRPORT_FLIGHTS_MONTH', 
    'AIRLINE_FLIGHTS_MONTH', 'AIRLINE_AIRPORT_FLIGHTS_MONTH', 
    'AVG_MONTHLY_PASS_AIRPORT', 'AVG_MONTHLY_PASS_AIRLINE', 
    'FLT_ATTENDANTS_PER_PASS', 'GROUND_SERV_PER_PASS', 'PLANE_AGE', 
    'LATITUDE', 'LONGITUDE', 'PRCP', 'SNOW', 'SNWD', 'TMAX', 'AWND', 
    'CARRIER_HISTORICAL', 'DEP_AIRPORT_HIST', 'DAY_HISTORICAL', 'DEP_BLOCK_HIST'
]

ALL_FEATURES = CATEGORICAL_COLS + NUMERICAL_COLS

TARGET_COL = 'DEP_DEL15'

class FlightDataPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.encoder = OrdinalEncoder(
            handle_unknown='use_encoded_value',
            unknown_value=-1
        )
        self.categorical_cols = CATEGORICAL_COLS
        self.numerical_cols = NUMERICAL_COLS
        self.top_categories_ = {}
        
    def fit(self, X, y=None):
        X_cat = X[self.categorical_cols].astype(str).fillna('UNKNOWN').copy()
        
        # Limit cardinality of high-cardinality columns (cardinality > 240)
        # to fit scikit-learn's HistGradientBoosting limit of 255 classes.
        for col in self.categorical_cols:
            n_unique = X_cat[col].nunique()
            if n_unique > 240:
                # Keep top 230 categories and map others to 'OTHER'
                top_cats = X_cat[col].value_counts().head(230).index.tolist()
                self.top_categories_[col] = set(top_cats)
                # Map rare values to 'OTHER'
                X_cat[col] = X_cat[col].apply(lambda x: x if x in self.top_categories_[col] else 'OTHER')
                
        # Fit ordinal encoder on the processed categorical columns
        self.encoder.fit(X_cat)
        
        # Save unique categories for frontend dropdown menus
        self.categories_ = {}
        for col, categories in zip(self.categorical_cols, self.encoder.categories_):
            self.categories_[col] = sorted(list(categories))
            if 'UNKNOWN' not in self.categories_[col]:
                self.categories_[col].append('UNKNOWN')
                
        return self
        
    def transform(self, X):
        X_out = X.copy()
        
        # Extract and copy categorical columns
        X_cat = X_out[self.categorical_cols].astype(str).fillna('UNKNOWN')
        
        # Apply cardinality limiting for high-cardinality columns
        for col in self.categorical_cols:
            if col in self.top_categories_:
                # Map rare values to 'OTHER'
                X_cat[col] = X_cat[col].apply(lambda x: x if x in self.top_categories_[col] else 'OTHER')
                
        encoded_cat = self.encoder.transform(X_cat)
        
        # Replace categorical columns with encoded integers
        for i, col in enumerate(self.categorical_cols):
            X_out[col] = encoded_cat[:, i]
            
        # Convert numerical columns to float
        for col in self.numerical_cols:
            if col in X_out.columns:
                X_out[col] = pd.to_numeric(X_out[col], errors='coerce')
                
        cols_to_keep = self.categorical_cols + self.numerical_cols
        return X_out[cols_to_keep]
