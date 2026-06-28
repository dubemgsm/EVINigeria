import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score

# Define paths
INPUT_PATH = "data/processed/evi_scores.csv"
OUTPUT_PATH = "data/processed/disruption_risk.csv"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

print("1. Loading features and creating target variable...")
df = pd.read_csv(INPUT_PATH)

# Define target variable proxy: 1 if high conflict OR high EVI (above median)
median_conflict = df['conflict_intensity'].median()
median_evi = df['evi_score'].median()
df['target'] = ((df['conflict_intensity'] > median_conflict) | (df['evi_score'] > median_evi)).astype(int)

# Define features
features_cols = ['conflict_intensity', 'population_pressure', 'school_density', 'proximity_to_conflict']
X = df[features_cols]
y = df['target']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("2. Training Random Forest Classifier on full dataset...")
# Max depth 4 and min samples split 3 to prevent overfitting on 65 samples
rf = RandomForestClassifier(n_estimators=150, max_depth=4, random_state=42)
rf.fit(X_scaled, y)

# Get predictions and probabilities
probs = rf.predict_proba(X_scaled)[:, 1]
preds = rf.predict(X_scaled)

print("\nModel Training Performance:")
print(classification_report(y, preds))
roc_auc = roc_auc_score(y, probs)
print(f"ROC-AUC Score: {roc_auc:.4f}")

# Feature importances
importances = rf.feature_importances_
print("\nFeature Importances:")
for col, imp in zip(features_cols, importances):
    print(f"- {col}: {imp:.4f}")

# Assemble final output
output_df = df[['state', 'lga', 'pcode']].copy()
output_df['disruption_probability'] = probs
output_df['disruption_risk_label'] = preds
output_df['actual_target_proxy'] = y

# Sort by disruption probability in descending order
output_df = output_df.sort_values(by='disruption_probability', ascending=False).reset_index(drop=True)

# Save output
output_df.to_csv(OUTPUT_PATH, index=False)
print(f"\nPredictive modeling complete. Saved {len(output_df)} rows to {OUTPUT_PATH}")

print("\nSample predictions (Top 10 highest risk):")
print(output_df.head(10))
