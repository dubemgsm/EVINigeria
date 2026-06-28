import os
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

# Define paths
INPUT_PATH = "data/processed/evi_scores.csv"
OUTPUT_PATH = "data/processed/clusters.csv"

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

print("1. Loading features from EVI scores...")
df = pd.read_csv(INPUT_PATH)

# Extract features for clustering
X = df[['conflict_intensity', 'population_pressure', 'school_density']].copy()

# Scale features to [0, 1] range for KMeans
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

print("2. Running KMeans Clustering (k=4)...")
# Fix random seed for reproducibility
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster_id'] = kmeans.fit_predict(X_scaled_df)

print("3. Profiling clusters and mapping to human labels...")
# Dynamic cluster labeling logic based on centroid characteristics:
# - 'Emergency': Highest conflict intensity
# - 'Expansion': Highest population pressure of remaining
# - 'Relatively stable': Highest school density of remaining
# - 'Infrastructure gap': Last remaining cluster (low conflict, low access)

cluster_means = df.groupby('cluster_id')[['conflict_intensity', 'population_pressure', 'school_density']].mean()
print("Cluster Centroid Means (Raw):")
print(cluster_means)

remaining_ids = list(range(4))

# 1. Identify 'Emergency'
emergency_id = cluster_means.loc[remaining_ids, 'conflict_intensity'].idxmax()
remaining_ids.remove(emergency_id)

# 2. Identify 'Expansion'
expansion_id = cluster_means.loc[remaining_ids, 'population_pressure'].idxmax()
remaining_ids.remove(expansion_id)

# 3. Identify 'Relatively stable'
stable_id = cluster_means.loc[remaining_ids, 'school_density'].idxmax()
remaining_ids.remove(stable_id)

# 4. The last one is 'Infrastructure gap'
gap_id = remaining_ids[0]

# Define mapping
mapping = {
    emergency_id: "Emergency",
    expansion_id: "Expansion",
    stable_id: "Relatively stable",
    gap_id: "Infrastructure gap"
}

print(f"\nDiscovered Cluster Mappings:")
for cid, label in mapping.items():
    print(f"Cluster {cid} -> {label}")

# Apply mapping
df['cluster_label'] = df['cluster_id'].map(mapping)

# Select columns to save
output_df = df[['state', 'lga', 'pcode', 'conflict_intensity', 'population_pressure', 'school_density', 'cluster_id', 'cluster_label']]

# Save output
output_df.to_csv(OUTPUT_PATH, index=False)
output_df.to_csv(os.path.join(os.path.dirname(OUTPUT_PATH), "clustered_lgas.csv"), index=False)
print(f"Clustering complete. Saved {len(output_df)} rows to {OUTPUT_PATH} and clustered_lgas.csv")

print("\nSample rows of clustered LGAs:")
print(output_df.head(10))
